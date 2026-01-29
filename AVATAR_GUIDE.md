# Avatar Replacement - Step-by-Step Guide

## Quick Reference

```
YOUR VIDEO (your face) + AVATAR VIDEO (blonde's face) = EXPORT (blonde with your mouth movements)
```

---

## STEP 1: Create Your Avatar Look (One-Time Setup)

**What you need:** A video of the avatar speaking (from Grok, etc.)

1. Open `overlaystudio.html` in browser
2. Find **"Avatar Replacement"** panel on the right
3. Click the **"+" Add** card
4. Enter a name (e.g., "Blonde Creator")
5. Click **"Upload Video"** → select your avatar video
6. Click **"Save Look"**
7. Wait for analysis to complete (shows progress for 5 grid levels)

**✓ Done when:** You see the avatar thumbnail in the grid with frame count

---

## STEP 2: Upload Your Source Video

**What you need:** Video of YOU talking (the face you want to replace)

1. Drag your video into the **main upload area** (left side)
2. Wait for **auto-analysis** to complete
   - Shows "Extracting Frames"
   - Shows "Grid Analysis Level 1/5" through "5/5"
3. Check the **analysis summary** shows all 5 grid levels

**✓ Done when:** You see "MULTI-SCALE ANALYSIS COMPLETE" with face/mouth regions

---

## STEP 3: Select Your Avatar

1. In the **"Avatar Replacement"** panel
2. Click your avatar thumbnail (e.g., "Blonde Creator")
3. Confirm checkmark appears on the selected look

**✓ Done when:** Selected look shows name and frame count below the grid

---

## STEP 4: Fine-Tune Position

Adjust these sliders to fit the avatar over your face:

| Setting | What it does | Typical value |
|---------|--------------|---------------|
| **Scale** | Size of avatar face | 0.9 - 1.2x |
| **Offset X** | Move left/right | -20 to +20px |
| **Offset Y** | Move up/down | -20 to +20px |
| **Edge Blend** | Soften edges | 10-25px |
| **Face Padding** | Extra coverage area | 15-30px |

---

## STEP 5: Enable & Export

1. In **Step 4: Export** section, toggle **"Avatar Enabled"** ON
2. Scroll down to the **"Export"** card
3. Click **"Export Video"**
4. Wait for export to complete (shows percentage)
5. File downloads as `.webm`

---

## Troubleshooting

### "No face detected"
- Make sure face is clearly visible in frame
- Try better lighting
- Face should be at least 20% of frame

### Avatar doesn't align
- Adjust Scale (smaller if avatar is too big)
- Adjust Offset X/Y to center it
- Increase Face Padding for more coverage

### Lip sync looks off
- Avatar video needs clear mouth movements
- Source video needs clear mouth movements
- Both videos should have similar mouth openness range

### Analysis stuck
- Refresh page and try again
- Check browser console (F12) for errors
- Make sure face-api.js loaded (shows "Ready" badge)

---

## File Locations

- **App:** `/Users/kcdacre8tor/Neon_Video_Overlay_Studio/overlaystudio.html`
- **This guide:** `/Users/kcdacre8tor/Neon_Video_Overlay_Studio/AVATAR_GUIDE.md`

---

## Quick Checklist

```
[ ] 1. Avatar video uploaded & analyzed
[ ] 2. Source video uploaded & analyzed
[ ] 3. Avatar selected (checkmark visible)
[ ] 4. Settings adjusted (scale, offset, blend)
[ ] 5. "Avatar Enabled" toggle is ON
[ ] 6. Click "Export Video"
```
