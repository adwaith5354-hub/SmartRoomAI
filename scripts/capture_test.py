#!/usr/bin/env python3
"""
Test script for Phase 1: capture a few frames from the camera stream
and save them as JPEG images in data/scans/<session_timestamp>/.
"""

import os
import time
from pathlib import Path
import cv2

# Import the CameraStream from the app package
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))  # add SmartRoomAI root
from app.camera import CameraStream


def main():
    # Configure source: change to 0 for local webcam, or set your tablet IP stream URL.
    # For demonstration, we try to use the first available webcam; if none, we exit.
    from app.camera import list_available_devices
    devices = list_available_devices()
    if devices:
        source = devices[0]
        print(f"Using webcam index {source}")
    else:
        # Fallback to a placeholder network stream – user must replace with actual IP.
        source = "http://192.168.137.254:8080/video"
        print(f"No webcam found, attempting network stream: {source}")

    cam = CameraStream(source=source, fps=1.0)  # 1 fps capture
    if not cam.start():
        print("Failed to start camera stream. Exiting.")
        return

    # Create output directory
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    out_dir = Path("data") / "scans" / f"session_{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Saving frames to: {out_dir.resolve()}")

    frame_count = 0
    max_frames = 10  # capture 10 frames for demo
    for frame in cam.frames():
        frame_path = out_dir / f"frame_{frame_count:04d}.jpg"
        cv2.imwrite(str(frame_path), frame)
        print(f"Saved {frame_path.name}")
        frame_count += 1
        if frame_count >= max_frames:
            break

    cam.stop()
    print("Capture complete.")


if __name__ == "__main__":
    main()