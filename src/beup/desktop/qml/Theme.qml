pragma Singleton
import QtQuick

QtObject {
    property bool motionEnabled: true

    readonly property string fontFamily: "Segoe UI Variable"

    // 2026 theme modes, driven from Main.qml bindings to AppController:
    //   themeMode: the persisted setting — "light" (Sáng), "dark" (Tối),
    //     "system" (Theo hệ thống) or "wallpaper" (Theo hình nền máy tính).
    //   systemThemeMode: the resolved Windows light/dark mode ("light"/"dark").
    //   wallpaperSource: file URL of the Windows desktop wallpaper, or ""
    //     when no wallpaper could be read.
    // Wallpaper mode always uses the dark palette (with a scrim over the
    // image in Main.qml) so text stays readable over any wallpaper.  When
    // wallpaper mode is selected but no wallpaper is available,
    // wallpaperActive is false and the app falls back to the dark palette.
    property string themeMode: "system"
    property string systemThemeMode: "dark"
    property string wallpaperSource: ""
    readonly property bool wallpaperActive: themeMode === "wallpaper" && wallpaperSource.length > 0
    readonly property bool isLight: themeMode === "light"
        || (themeMode === "system" && systemThemeMode === "light")
    readonly property color wallpaperScrim: "#B3000000"

    // Dark palette: the original Warm Graphite Studio values, unchanged.
    // Neutral surfaces carry hierarchy; copper is reserved for direct
    // interaction, focus and progress.
    readonly property QtObject darkPalette: QtObject {
        property color window: "#11100F"
        property color surface: "#1B1A18"
        property color surfaceElevated: "#211F1C"
        property color surfaceMuted: "#292620"
        property color surfaceStrong: "#302C27"
        property color input: "#171614"
        property color sidebar: "#161513"
        property color sidebarHover: "#211F1C"
        property color sidebarSelected: "#302820"
        property color topBar: "#161513"
        property color windowCaptionHover: "#292620"
        property color windowCaptionPressed: "#332F2A"
        property color outline: "#48423A"
        property color outlineStrong: "#665F55"
        property color divider: "#332F2A"
        property color text: "#F2EFE9"
        property color textMuted: "#B8B1A6"
        property color textSubtle: "#91897D"
        property color textDisabled: "#797268"
        property color interactiveMuted: "#33271D"
        property color focus: "#E2B47F"
        property color controlFocus: "#B8B1A6"
        property color amber: "#C29A57"
        property color amberMuted: "#3B3020"
        property color warmSurface: "#211F1C"
        property color danger: "#C96F68"
        property color dangerMuted: "#3D2421"
        property color success: "#76A58A"
        property color successMuted: "#22352A"
        property color warning: "#C29A57"
        property color warningMuted: "#3B3020"
    }

    // Light palette: warm paper, not an inversion of the dark palette.
    // Muted text is a dark warm grey (not a lightened dark-mode grey) so
    // it keeps at least 4.5:1 contrast on light surfaces.
    readonly property QtObject lightPalette: QtObject {
        property color window: "#F4F0E8"
        property color surface: "#FDFBF7"
        property color surfaceElevated: "#FFFFFF"
        property color surfaceMuted: "#EDE7DB"
        property color surfaceStrong: "#E2DACA"
        property color input: "#FFFFFF"
        property color sidebar: "#EFE9DD"
        property color sidebarHover: "#E7DFD1"
        property color sidebarSelected: "#E3D3BE"
        property color topBar: "#EFE9DD"
        property color windowCaptionHover: "#E7DFD1"
        property color windowCaptionPressed: "#DCD2BF"
        property color outline: "#D8CFC0"
        property color outlineStrong: "#B9AC96"
        property color divider: "#E3DCCF"
        property color text: "#211D17"
        property color textMuted: "#5C554A"
        property color textSubtle: "#7A7264"
        property color textDisabled: "#A79E8E"
        property color interactiveMuted: "#F0E2CE"
        property color focus: "#8A5A2B"
        property color controlFocus: "#6B6154"
        property color amber: "#8A5A2B"
        property color amberMuted: "#F3E7CE"
        property color warmSurface: "#F3EDE2"
        property color danger: "#B3261E"
        property color dangerMuted: "#F6DDD9"
        property color success: "#2E7D4F"
        property color successMuted: "#DDEEE3"
        property color warning: "#8A5A2B"
        property color warningMuted: "#F3E7CE"
    }

    // Every pre-existing Theme.* color name still exists; palette colours
    // resolve from the active palette, shared colours stay literal.
    readonly property color window: isLight ? lightPalette.window : darkPalette.window
    readonly property color surface: isLight ? lightPalette.surface : darkPalette.surface
    readonly property color surfaceElevated: isLight ? lightPalette.surfaceElevated : darkPalette.surfaceElevated
    readonly property color surfaceMuted: isLight ? lightPalette.surfaceMuted : darkPalette.surfaceMuted
    readonly property color surfaceStrong: isLight ? lightPalette.surfaceStrong : darkPalette.surfaceStrong
    readonly property color input: isLight ? lightPalette.input : darkPalette.input
    readonly property color sidebar: isLight ? lightPalette.sidebar : darkPalette.sidebar
    readonly property color sidebarHover: isLight ? lightPalette.sidebarHover : darkPalette.sidebarHover
    readonly property color sidebarSelected: isLight ? lightPalette.sidebarSelected : darkPalette.sidebarSelected
    readonly property color topBar: isLight ? lightPalette.topBar : darkPalette.topBar
    readonly property color windowCaptionHover: isLight ? lightPalette.windowCaptionHover : darkPalette.windowCaptionHover
    readonly property color windowCaptionPressed: isLight ? lightPalette.windowCaptionPressed : darkPalette.windowCaptionPressed
    readonly property color windowCloseHover: "#c42b1c"
    readonly property color windowClosePressed: "#a4262c"
    readonly property color outline: isLight ? lightPalette.outline : darkPalette.outline
    readonly property color outlineStrong: isLight ? lightPalette.outlineStrong : darkPalette.outlineStrong
    readonly property color divider: isLight ? lightPalette.divider : darkPalette.divider

    readonly property color text: isLight ? lightPalette.text : darkPalette.text
    readonly property color textMuted: isLight ? lightPalette.textMuted : darkPalette.textMuted
    readonly property color textSubtle: isLight ? lightPalette.textSubtle : darkPalette.textSubtle
    readonly property color textDisabled: isLight ? lightPalette.textDisabled : darkPalette.textDisabled
    readonly property color textOnAccent: "#17120D"
    readonly property color textOnDark: "#F2EFE9"
    readonly property color textOnDarkMuted: "#B8B1A6"

    readonly property color interactive: "#C4915E"
    readonly property color interactiveHover: "#D4A16B"
    readonly property color interactivePressed: "#A9784A"
    readonly property color interactiveMuted: isLight ? lightPalette.interactiveMuted : darkPalette.interactiveMuted
    readonly property color interactiveOutline: "#7B5B3C"
    readonly property color focus: isLight ? lightPalette.focus : darkPalette.focus
    // Neutral keyboard focus for controls; copper still marks selected content.
    readonly property color controlFocus: isLight ? lightPalette.controlFocus : darkPalette.controlFocus

    readonly property color amber: isLight ? lightPalette.amber : darkPalette.amber
    readonly property color amberMuted: isLight ? lightPalette.amberMuted : darkPalette.amberMuted
    readonly property color warmSurface: isLight ? lightPalette.warmSurface : darkPalette.warmSurface
    readonly property color danger: isLight ? lightPalette.danger : darkPalette.danger
    readonly property color dangerMuted: isLight ? lightPalette.dangerMuted : darkPalette.dangerMuted
    readonly property color success: isLight ? lightPalette.success : darkPalette.success
    readonly property color successMuted: isLight ? lightPalette.successMuted : darkPalette.successMuted
    readonly property color warning: isLight ? lightPalette.warning : darkPalette.warning
    readonly property color warningMuted: isLight ? lightPalette.warningMuted : darkPalette.warningMuted
    readonly property color scrim: "#b8000000"
    readonly property color video: "#080706"
    readonly property color codeSurface: "#0D0C0B"
    readonly property color codeText: "#D0CAC1"
    readonly property color captionOverlay: "#DC11100F"
    readonly property color captionText: "#FFFFFF"

    // 2026 radii: 12 for cards/dialogs, 8 for controls, 6 for tiny inner
    // elements.  Components that use Theme.radius / radiusSmall (AppSurface,
    // AppDialog, AppButton, SegmentedControl, ...) pick these up as-is.
    readonly property int radius: 12
    readonly property int radiusSmall: 8
    readonly property int radiusTiny: 6

    readonly property int space4: 4
    readonly property int space8: 8
    readonly property int space12: 12
    readonly property int space16: 16
    readonly property int space20: 20
    readonly property int space24: 24
    readonly property int space32: 32
    readonly property int gap: space16

    readonly property int label: TypeScale.metadata
    readonly property int caption: TypeScale.label
    readonly property int body: TypeScale.control
    readonly property int bodyLarge: TypeScale.body
    readonly property int h3: TypeScale.section
    readonly property int h2: TypeScale.title
    readonly property int h1: TypeScale.pageTitle
    readonly property int display: TypeScale.display

    readonly property int iconSmall: 14
    readonly property int icon: 16
    readonly property int iconLarge: 20
    readonly property string iconFont: "Segoe Fluent Icons"

    readonly property int motionFast: motionEnabled ? Motion.fast : 0
    readonly property int motionStandard: motionEnabled ? Motion.standard : 0
    readonly property int motionSlow: motionEnabled ? Motion.slow : 0
    readonly property int navigationExpanded: UiMetrics.navigationExpanded
    readonly property int navigationCompact: UiMetrics.navigationCompact
    readonly property int commandBarHeight: 48
}
