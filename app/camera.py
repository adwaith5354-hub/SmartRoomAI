"""
Camera handling for SmartRoom AI Phase 1.
Supports local webcam (index) or network stream (IP Webcam on Android).
"""

import cv2
import time
from typing import Generator, Optional


class CameraStream:
    """
    Captures frames from a video source.

    Parameters
    ----------
    source : int or str
        Either a device index (e.g., 0 for default webcam) or a URL
        (e.g., "http://192.168.1.42:8080/video" for IP Webcam MJPEG stream).
    fps : float, optional
        Desired frames per second to yield. If None, yields every captured frame.
    """

    def __init__(self, source: int | str = 0, fps: Optional[float] = 1.0):
        self.source = source
        self.fps = fps
        self._cap = None
        self._frame_interval = 1.0 / fps if fps and fps > 0 else 0
        self._last_grab = 0.0

    def start(self) -> bool:
        """Open the video source. Returns True if successful."""
        self._cap = cv2.VideoCapture(self.source)
        if not self._cap.isOpened():
            print(f"[CameraStream] Failed to open source: {self.source}")
            self._cap = None
            return False
        print(f"[CameraStream] Opened source: {self.source}")
        return True

    def read(self) -> Optional[cv2.Mat]:
        """
        Grab a single frame, respecting the desired fps.
        Returns None if no frame is available or if end of stream.
        """
        if self._cap is None or not self._cap.isOpened():
            return None

        # If we are limiting fps, wait until enough time has passed.
        if self._frame_interval > 0:
            now = time.time()
            if now - self._last_grab < self._frame_interval:
                return None
            self._last_grab = now

        ret, frame = self._cap.read()
        if not ret:
            return None
        return frame

    def frames(self) -> Generator[cv2.Mat, None, None]:
        """
        Generator that yields frames continuously until the stream ends
        or the camera is released.
        """
        while True:
            frame = self.read()
            if frame is None:
                # If the stream is exhausted (e.g., video file ended) we may break.
                # For live sources (webcam or HTTP stream) we keep trying.
                if isinstance(self.source, str) and self.source.startswith("http"):
                    # brief pause before retrying network stream
                    time.sleep(0.5)
                    continue
                # For device indices, treat None as a temporary read failure; continue.
                # Optionally, after many consecutive failures we could break.
                continue
            yield frame

    def stop(self) -> None:
        """Release the video capture resource."""
        if self._cap is not None:
            self._cap.release()
            self._cap = None
            print("[CameraStream] Video source released.")


def list_available_devices(max_to_check: int = 5) -> list[int]:
    """
    Probe for available webcam indices.
    Returns a list of indices that OpenCV can open.
    """
    available = []
    for idx in range(max_to_check):
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            available.append(idx)
            cap.release()
    return available


if __name__ == "__main__":
    # Simple demo: list webcams, then capture from first available or fallback to URL.
    print("Available webcam indices:", list_available_devices())
    # Example usage: uncomment one of the following lines to test.
    # cam = CameraStream(source=0)          # local webcam
    # cam = CameraStream(source="http://<TABLET_IP>:8080/video")  # IP Webcam
    # if cam.start():
    #     for i, frame in enumerate(cam.frames()):
    #         cv2.imshow("SmartRoom AI - Live Feed", frame)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #         if i >= 300:  # limit demo frames
    #             break
    #     cam.stop()
    #     cv2.destroyAllWindows()