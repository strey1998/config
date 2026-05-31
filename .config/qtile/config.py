import os
from pathlib import Path
from collections.abc import Callable
import json

import libqtile.resources
from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Output, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from custom.widgets.baseballscores import BaseballScores

mod = "mod4"
terminal = guess_terminal()

with open(f"{Path.home()}/.cache/wal/colors.json", 'r') as file:
    wal_config = json.load(file)
background_color = wal_config["special"]["background"]
foreground_color = wal_config["special"]["foreground"]
cursor_color = wal_config["special"]["cursor"]

colors = ["#000000"] * len(wal_config["colors"])
for key in wal_config["colors"]:
    index = int(key[5:])
    colors[index] = wal_config["colors"][key]

bar_background_color = colors[1]

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "control"], "b",  lazy.spawn("brave"), desc="Launch web browser"),
    # Key([mod, "control", "shift"], "f",  lazy.spawn("firefox --private-window"), desc="Launch private web browser"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn('/usr/bin/rofi -modes "run" -show'), desc="Spawn a command using a prompt widget"),
    Key([mod], "e", lazy.spawn('/usr/bin/rofi -modes "window" -show'), desc="Find a window"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_config = {
    "border_width": 2,
    "margin": 7,
    "border_focus": foreground_color,
    "border_normal": colors[2],
    "border_focus_stack": foreground_color,
    "border_normal_stack": colors[2],
    "font": "MesloLGS Nerd Font Mono",
    "grow_amount": 2,
}

layouts = [
    layout.Bsp(**layout_config, fair=False, border_on_single=True),
    layout.Columns(**layout_config, border_on_single=True, columns=2, split=False),
    layout.Floating(**layout_config),
    layout.Zoomy(**layout_config),
    layout.Max(**layout_config),
]

widget_defaults = dict(
    font="MesloLGS Nerd Font Mono",
    fontsize=24,
    padding=3,
)
extension_defaults = widget_defaults.copy()

logo = os.path.join(os.path.dirname(libqtile.resources.__file__), "logo.png")
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(length=15),
                widget.CryptoTicker(crypto='BTC', update_interval=60),
                widget.CryptoTicker(crypto='ETH', update_interval=60),
                widget.CryptoTicker(crypto='XRP', update_interval=60),
#                widget.Sep(),
#                BaseballScores(team_id=146, update_interval=30),
#                widget.Sep(),
#                BaseballScores(team_id=116, update_interval=30),
#                widget.Sep(),
#                BaseballScores(team_id=139, update_interval=30),
#                widget.Sep(),
#                BaseballScores(team_id=143, update_interval=30),
                widget.Sep(),
                BaseballScores(team_id=111, update_interval=30),
                widget.Sep(),
                BaseballScores(team_id=140, update_interval=30),
                widget.Sep(),
                BaseballScores(team_id=135, update_interval=30),
                widget.Spacer(),
                widget.NetGraph(border_color=colors[2], graph_color=foreground_color, fill_color=f"{foreground_color}.3"),
                widget.Net(),
                widget.CPUGraph(border_color=colors[2], graph_color=foreground_color, fill_color=f"{foreground_color}.3"),
                widget.CPU(),
                widget.MemoryGraph(border_color=colors[2], graph_color=foreground_color, fill_color=f"{foreground_color}.3"),
                widget.Memory(),
                widget.SwapGraph(border_color=colors[2], graph_color=foreground_color, fill_color=f"{foreground_color}.3"),
                widget.Memory(format='{SwapUsed: .0f}{ms}/{SwapTotal: .0f}{ms}'),
                widget.Spacer(length=15),
            ],
            48,
            background=bar_background_color,
            margin=[7, 7, 0, 7],
        ),
        bottom=bar.Bar(
            [
                widget.Spacer(length=15),
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(),
                widget.Clock(format="%a %d %b %H:%M:%S %Z", update_interval=0.02),
                widget.QuickExit(),
                widget.Spacer(length=15),
            ],
            48,
            background=bar_background_color,
            margin=[0, 7, 7, 7],
        ),
        background=background_color,
        wallpaper=wal_config["wallpaper"],
        wallpaper_mode="center",
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Instead of screens, you can define a function here to specify which Screen
# should correspond to which Output.
fake_screens: list[Screen] | None = None

# Instead of screens or fake screens, you can define a function here that
# returns a list of Screen objects based on the list of Outputs; that way you
# can decide based on e.g. the number of screens, or which ports are plugged
# in exactly what do render in each bar for each screen.
generate_screens: Callable[[list[Output]], list[Screen]] | None = None

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

import subprocess

@hook.subscribe.startup_once
def startup_once():
    subprocess.call([f"{Path.home()}/.config/qtile/startup_once.sh"])

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

idle_timers = []  # type: list
idle_inhibitors = []  # type: list

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
