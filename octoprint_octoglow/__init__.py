# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import octoprint.events
import time
import threading
from .piglow import PiGlow

class OctoGlowPlugin(octoprint.plugin.EventHandlerPlugin,
                     octoprint.plugin.ProgressPlugin,
                     octoprint.plugin.ShutdownPlugin,
                     octoprint.plugin.StartupPlugin):
    """
    Plugin for animating the LEDs on a PiGlow board based on OctoPrint events.
    """

    def __init__(self):
        self._piglow = PiGlow()

        self._lock = threading.Lock()
        self._currentAnimation = None
        self._printProgress = 0

        self._animator = threading.Thread(target=self._animate)
        self._animator.daemon = True


    def on_after_startup(self):
        """
        Callback for just after launch of OctoPrint.
        """
        self._logger.info("OctoGlow startup")
        self._animator.start()

    def on_shutdown(self):
        """
        Callback for imminent shutdown of OctoPrint.
        """
        self._logger.info("OctoGlow shutdown")

    def on_event(self, event, payload):
        """
        Callback for general OctoPrint events.
        """
        with self._lock:
            if event == octoprint.events.Events.CONNECTED:
                self._currentAnimation = self._animatePrinterConnected
            elif event == octoprint.events.Events.PRINT_STARTED:
                self._currentAnimation = self._animatePrintStarted
            elif event == octoprint.events.Events.PRINT_DONE:
                self._currentAnimation = self._animatePrintDone
            elif event == octoprint.events.Events.PRINT_FAILED or event == octoprint.events.Events.PRINT_CANCELLED:
                self._currentAnimation = self._animatePrintFailed
            elif event == octoprint.events.Events.DISCONNECTED:
                self._currentAnimation = None
            
    def on_printProgress(self, storage, path, progress):
        """
        Callback for progress during a running print job.
        """
        with self._lock:
            self._currentAnimation = self._animatePrintProgress
            self._printProgress = progress

    def _animate(self):
        """
        Handle a frame of animation.
        """
        
        frame = 0
        printProgress = 0

        while True:
            if frame == 0:
                with self._lock:
                    currentAnimation = self._currentAnimation
                    printProgress = self._printProgress

            if currentAnimation is not None:
                frame = currentAnimation(frame, printProgress)

            time.sleep(0.03)

    def _animatePrintDone(self, frame, printProgress):
        """
        Handle a frame of the print done animation.
        """
        return self._pulse("green", frame, printProgress)

    def _animatePrinterConnected(self, frame, printProgress):
        """
        Handle a frame of the printer connected animation.
        """
        return self._pulse("white", frame, printProgress)

    def _pulse(self, colour, frame, printProgress):
        """
        Handle a frame of the pulse animation.
        """
        next_frame = frame + 1;

        if frame < 64:
            self._piglow.colour(colour, frame)
        elif frame < 128:
            self._piglow.colour(colour, 64 - (frame - 64))
        else:
            next_frame = 0

        return next_frame

    def _animatePrintFailed(self, frame, printProgress):
        """
        Handle a frame of the print failed animation.
        """
        next_frame = frame + 1;

        if frame < 16:
            self._piglow.colour(colour, 128)
        elif frame < 32:
            self._piglow.colour(colour, 0)
        elif frame < 48:
            self._piglow.colour(colour, 128)
        elif frame < 128:
            self._piglow.colour(colour, 0)
        else:
            next_frame = 0

        return next_frame

    def _animatePrintStarted(self, frame, printProgress):
        """
        Handle a frame of the print started animation.
        """
        next_frame = frame + 1;

        if frame < 32:
            self._piglow.arm1(32)
        elif frame < 64:
            self._piglow.arm1(0)
            self._piglow.arm2(32)
        elif frame < 96:
            self._piglow.arm2(0)
            self._piglow.arm3(32)
        else:
            self._piglow.arm3(0)
            next_frame = 0

        return next_frame

    def _animatePrintProgress(self, frame, printProgress):
        """
        Handle a frame of the print progress animation.
        """
        next_frame = frame + 1;
        level = frame;

        if frame > 32:
            level = 32 - (frame - 32)
        elif frame > 64:
            next_frame = 0

        piglow.white(level)
        if printProgress > 20:
            piglow.blue(level)
        if printProgress > 40:
            piglow.green(level)
        if printProgress > 60:
            piglow.yellow(level)
        if printProgress > 80:
            piglow.orange(level)

__plugin_name__ = "OctoGlow"
__plugin_implementations__ = [OctoGlowPlugin()]
