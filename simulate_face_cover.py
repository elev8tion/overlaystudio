#!/usr/bin/env python3
"""
Simulate Face Cover - Preview face replacement before using the UI
"""

import cv2
import numpy as np
import os

# File paths
VIDEO_PATH = "/Users/kcdacre8tor/Downloads/0636e60e-f505-41a2-904b-6deee4fa717a_00-05.00-00-17.87_processed.webm"
AVATAR_PATH = "/Users/kcdacre8tor/Downloads/Subject.png"
OUTPUT_DIR = "/Users/kcdacre8tor/Neon_Video_Overlay_Studio/simulation_output"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the avatar image
avatar = cv2.imread(AVATAR_PATH, cv2.IMREAD_UNCHANGED)
if avatar is None:
    print(f"Error: Could not load avatar from {AVATAR_PATH}")
    exit(1)

print(f"Avatar loaded: {avatar.shape}")

# Load video
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print(f"Error: Could not open video {VIDEO_PATH}")
    exit(1)

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Fix fps if it's unrealistic
if fps > 60:
    fps = 30

print(f"Video: {width}x{height}, {fps} fps, {total_frames} frames")

# Use multiple face cascades for better detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
face_cascade_alt = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

def detect_faces(frame):
    """Detect faces in frame using multiple cascades"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)  # Improve contrast

    # Try default cascade with relaxed params
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(30, 30))

    if len(faces) == 0:
        # Try alt2 cascade
        faces = face_cascade_alt.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(30, 30))

    if len(faces) == 0:
        # Try profile cascade
        faces = profile_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(30, 30))

    return faces

def overlay_avatar(frame, face_rect, avatar_img, padding=30):
    """Overlay avatar on detected face area"""
    x, y, w, h = face_rect

    # Add padding
    x = max(0, x - padding)
    y = max(0, y - padding)
    w = min(frame.shape[1] - x, w + padding * 2)
    h = min(frame.shape[0] - y, h + padding * 2)

    # Resize avatar to fit face area
    avatar_resized = cv2.resize(avatar_img, (w, h))

    # Handle alpha channel if present
    if avatar_resized.shape[2] == 4:
        alpha = avatar_resized[:, :, 3] / 255.0
        alpha = np.stack([alpha] * 3, axis=-1)
        roi = frame[y:y+h, x:x+w]
        avatar_rgb = avatar_resized[:, :, :3]
        blended = (alpha * avatar_rgb + (1 - alpha) * roi).astype(np.uint8)
        frame[y:y+h, x:x+w] = blended
    else:
        frame[y:y+h, x:x+w] = avatar_resized

    return frame

def apply_blur(frame, face_rect, blur_strength=51, padding=30):
    """Apply blur to face area"""
    x, y, w, h = face_rect
    x = max(0, x - padding)
    y = max(0, y - padding)
    w = min(frame.shape[1] - x, w + padding * 2)
    h = min(frame.shape[0] - y, h + padding * 2)

    roi = frame[y:y+h, x:x+w]
    blurred = cv2.GaussianBlur(roi, (blur_strength, blur_strength), 0)
    frame[y:y+h, x:x+w] = blurred
    return frame

def apply_pixelate(frame, face_rect, pixel_size=15, padding=30):
    """Apply pixelation to face area"""
    x, y, w, h = face_rect
    x = max(0, x - padding)
    y = max(0, y - padding)
    w = min(frame.shape[1] - x, w + padding * 2)
    h = min(frame.shape[0] - y, h + padding * 2)

    roi = frame[y:y+h, x:x+w]
    small = cv2.resize(roi, (max(1, w // pixel_size), max(1, h // pixel_size)), interpolation=cv2.INTER_LINEAR)
    pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    frame[y:y+h, x:x+w] = pixelated
    return frame

# Read frames properly (WebM can be tricky)
print("\nReading video frames...")
frames = []
while len(frames) < 100:  # Get first 100 frames
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)

print(f"Read {len(frames)} frames")

if len(frames) == 0:
    print("Error: No frames read from video")
    exit(1)

# Save first frame to check content
cv2.imwrite(f"{OUTPUT_DIR}/check_frame_0.png", frames[0])
print(f"Saved first frame to check content")

# Process sample frames
sample_indices = [0, len(frames)//4, len(frames)//2, 3*len(frames)//4]
print(f"\nProcessing sample frames: {sample_indices}")

all_faces_found = []
for idx in sample_indices:
    if idx >= len(frames):
        continue

    frame = frames[idx]
    faces = detect_faces(frame)
    print(f"Frame {idx}: Found {len(faces)} face(s)")

    if len(faces) > 0:
        all_faces_found.extend(faces)

        frame_blur = frame.copy()
        frame_pixel = frame.copy()
        frame_avatar = frame.copy()
        frame_original = frame.copy()

        for face in faces:
            frame_blur = apply_blur(frame_blur, face, blur_strength=51, padding=50)
            frame_pixel = apply_pixelate(frame_pixel, face, pixel_size=12, padding=50)
            frame_avatar = overlay_avatar(frame_avatar, face, avatar, padding=50)

            x, y, w, h = face
            cv2.rectangle(frame_original, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame_original, "Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imwrite(f"{OUTPUT_DIR}/frame_{idx:04d}_original.png", frame_original)
        cv2.imwrite(f"{OUTPUT_DIR}/frame_{idx:04d}_blur.png", frame_blur)
        cv2.imwrite(f"{OUTPUT_DIR}/frame_{idx:04d}_pixelate.png", frame_pixel)
        cv2.imwrite(f"{OUTPUT_DIR}/frame_{idx:04d}_avatar.png", frame_avatar)
        print(f"  Saved 4 versions for frame {idx}")

# If no faces found automatically, create manual preview with estimated position
if len(all_faces_found) == 0:
    print("\nNo faces auto-detected. Creating manual preview with estimated face position...")

    # For vertical video with person talking, face is typically in upper-middle area
    # Estimate face region (adjust these for your video)
    estimated_face = (width//4, height//8, width//2, height//2)  # x, y, w, h

    frame = frames[len(frames)//2].copy()

    # Create versions with estimated position
    frame_blur = frame.copy()
    frame_pixel = frame.copy()
    frame_avatar = frame.copy()

    frame_blur = apply_blur(frame_blur, estimated_face, blur_strength=51, padding=0)
    frame_pixel = apply_pixelate(frame_pixel, estimated_face, pixel_size=15, padding=0)
    frame_avatar = overlay_avatar(frame_avatar, estimated_face, avatar, padding=0)

    cv2.imwrite(f"{OUTPUT_DIR}/manual_blur.png", frame_blur)
    cv2.imwrite(f"{OUTPUT_DIR}/manual_pixelate.png", frame_pixel)
    cv2.imwrite(f"{OUTPUT_DIR}/manual_avatar.png", frame_avatar)

    # Draw estimated region on original
    x, y, w, h = estimated_face
    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(frame, "Estimated face area", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.imwrite(f"{OUTPUT_DIR}/manual_original.png", frame)

    print("Saved manual preview with estimated face position")

# Create comparison grid
print("\nCreating comparison image...")
if len(frames) > 0:
    frame = frames[len(frames)//2].copy()

    # Determine face region to use
    if len(all_faces_found) > 0:
        face = all_faces_found[0]
    else:
        face = (width//4, height//8, width//2, height//2)

    orig = frame.copy()
    blur = apply_blur(frame.copy(), face, blur_strength=51, padding=50)
    pixel = apply_pixelate(frame.copy(), face, pixel_size=12, padding=50)
    avatar_frame = overlay_avatar(frame.copy(), face, avatar, padding=50)

    # Create 2x2 grid
    top_row = np.hstack([cv2.resize(orig, (width//2, height//2)),
                         cv2.resize(blur, (width//2, height//2))])
    bottom_row = np.hstack([cv2.resize(pixel, (width//2, height//2)),
                           cv2.resize(avatar_frame, (width//2, height//2))])
    grid = np.vstack([top_row, bottom_row])

    # Add labels
    cv2.putText(grid, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(grid, "Blur", (width//2 + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(grid, "Pixelate", (10, height//2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(grid, "Avatar", (width//2 + 10, height//2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imwrite(f"{OUTPUT_DIR}/comparison_grid.png", grid)
    print("Saved comparison_grid.png")

cap.release()
print(f"\nDone! Check output at: {OUTPUT_DIR}")
