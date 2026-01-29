# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Neon Video Overlay Studio is a React-based single-page application for applying neon-themed visual overlays to MP4 videos. The entire application is contained in `overlaystudio.html` - a self-contained React component file that uses JSX syntax.

## Architecture

**Single-file React application** (`overlaystudio.html`):
- Uses React hooks (`useState`, `useRef`, `useEffect`) for state management
- Imports UI components from `@/components/ui` (shadcn/ui pattern)
- Uses Lucide React for icons

**Key data structures:**
- `OVERLAY_LIST`: Array of 18 overlay definitions, each with a key, name, tooltip, and SVG preview
- `overlayStyles`: Maps overlay keys to CSS class names
- `OverlayDiv`: Main overlay renderer - a switch statement dispatching to overlay-specific JSX based on type

**Overlay types** (all rendered as positioned absolute divs with SVG/CSS animations):
- Grid variants: cyber-grid, fine-grid, bold-grid, hex-grid, diagonal-grid, dot-grid
- Effect overlays: motion-outline, glitch-effect, holographic, matrix-rain, vhs-retro, neon-glow, scan-lines, chromatic-aberration, film-grain, vaporwave, futuristic-hud, particle-dust

**State flow:**
1. User uploads MP4 → stored in `videoFile` state, blob URL in `videoUrl`
2. User selects overlay from panel → `selectedOverlay` state updated
3. `OverlayDiv` renders selected overlay on top of video with `overlayIntensity` opacity
4. Toggle switch controls `overlayOn` visibility

## Key Components

- `VideoOverlayStudio`: Main component managing all state and UI layout
- `OverlayDiv`: Renders overlay effects based on type prop
- `AnimatedOutline`: SVG path animation for motion-outline effect
- `MatrixColumn`: Animated falling character column for matrix-rain effect

## Styling

All CSS is embedded in a `<style>` block at the end of the component:
- `.glassy`: Glassmorphism effect with blur
- `.drop-shadow-glow`: Neon glow effects
- Various `@keyframes` for animations (cybergrid-vert, outlinepulse, matrix-fall, etc.)
- Responsive breakpoints at 900px, 700px, 550px, 520px, 500px

## Development Notes

- The `eng.traineddata` file is Tesseract OCR training data (not part of the React app)
- Video export functionality has been optimized for 4-6x faster MP4 conversion (per git history)
- Logo overlay was added then removed from exports

## Key Features

**Video Export with Overlay**: Uses Canvas API and MediaRecorder to bake overlays into exported WebM files. Frame-by-frame rendering with `drawOverlayOnCanvas()` function.

**Mutable Overlay Settings**:
- `primaryColor`, `secondaryColor`, `tertiaryColor`: Hex color values
- `animationSpeed`: Multiplier for animation timing (0.1-3x)
- `lineThickness`: Multiplier for stroke widths (0.1-3x)
- `glowIntensity`: Multiplier for shadow/glow effects (0-3x)
- `density`: Multiplier for element count/spacing (0.2-3x)

**Fine Intensity Control**: Slider with 0.001 step + numeric input for precise values.

## Working with This Codebase

When modifying overlays:
1. Add new overlay definition to `OVERLAY_LIST` with SVG preview
2. Add rendering case to `OverlayDiv` switch statement (use settings props)
3. Add canvas rendering case to `drawOverlayOnCanvas()` for export support
4. Add any required CSS keyframes to the embedded style block
