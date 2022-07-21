# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import subprocess
from typing import List  # noqa: F401
import psutil

from libqtile.config import (
    Key,
    Screen,
    Group,
    Drag,
    Click,
    ScratchPad,
    DropDown,
    Match,
)
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile import qtile
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
from qtile_extras.widget.decorations import RectDecoration

# from plasma import Plasma


mod = "mod4"
terminal = "kitty"


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    # Floating layout controls
    Key(
        [mod],
        "BackSpace",
        lazy.group.next_window(),
        lazy.window.bring_to_front(),
        desc="Cycle next floating windows"),
    
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
    Key([mod], "a", lazy.spawn("./.config/rofi/launchers/text/launcher.sh"), desc="Rofi app launcher"),
    Key([mod], "p", lazy.spawn("./.config/rofi/powermenu/powermenu.sh"), desc="Rofi powermenu"),    
    Key([mod], "f", lazy.spawn("firefox"), desc="Launch firefox"),
    Key([mod], "t", lazy.spawn("thunar"), desc="Launch thunar"),
    Key([], "Print", lazy.spawn("flameshot screen"), desc="Print Screen"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +10%"), desc="Increase volume",),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%"), desc="Decrease volume",),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Toggle mute",),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s 5%+"), desc="Increase brightness",),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 5%-"), desc="Decrease Volume",),
    Key([mod], "v", lazy.spawn("code"), desc="Launch vs code"),
    
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    #Key( [mod, "shift"],"e",lazy.spawn("power"),desc="Power Menu"),
    
 
]


workspaces = [
    {"name": "", "key": "1", "matches": [Match(wm_class="firefox")], "lay": "columns"},
    {"name": "", "key": "2", "matches": [Match(wm_class="kitty")], "lay": "spiral"},
    {"name": "", "key": "3", "matches": [Match(wm_class="Gedit"), Match(wm_class="Code")], "lay": "columns"},
    {"name": "", "key": "4", "matches":[Match(wm_class="libreoffice"), Match(wm_class="Zathura"), Match(wm_class="Xournalpp"), Match(wm_class="Joplin")], "lay": "columns"},
    {"name": "", "key": "5", "matches": [Match(wm_class="TelegramDesktop")], "lay": "columns"},
    {"name": "", "key": "6", "matches": [Match(wm_class="vlc")], "lay": "columns"},
    {"name": "", "key": "7", "matches": [Match(wm_class="calibre"), Match(wm_class="homebank")], "lay": "columns"},
    {"name": "", "key": "8", "matches": [Match(wm_class="Thunar")], "lay": "columns"},
    {"name": "", "key": "9", "matches": [Match(wm_class="Gimp-2.10"), Match(wm_class="krita")],"lay": "columns"},
    {"name": "", "key": "0", "matches": [Match(wm_class="Pavucontrol")],"lay": "floating"},
]

groups = [
    ScratchPad(
        "scratchpad",
        [
            # define a drop down terminal.
            DropDown(
                "term",
                "kitty",
                height=0.6,
                on_focus_lost_hide=False,
                opacity=1,
                warp_pointer=False,
            ),
        ],
    ),
]

for workspace in workspaces:
    matches = workspace["matches"] if "matches" in workspace else None
    groups.append(Group(workspace["name"], matches=matches, layout=workspace["lay"]))
    keys.append(
        Key(
            [mod],
            workspace["key"],
            lazy.group[workspace["name"]].toscreen(toggle=True),
            desc="Focus this desktop",
        )
    )
    keys.append(
        Key(
            [mod, "shift"],
            workspace["key"],
            lazy.window.togroup(workspace["name"]),
            desc="Move focused window to another group",
        )
    )


# Define colors

colors = [
    ["#121216", "#121216"],  # 0 background
    ["#EAF4F4", "#EAF4F4"],  # 1 foreground
    ["#333D47", "#333D47"],  # 2 background lighter
    ["#FE3D20", "#FE3D20"],  # 3 red
    ["#39FF14", "#39FF14"],  # 4 green
    ["#FFFC47", "#FFFC47"],  # 5 yellow
    ["#90E0EF", "#90E0EF"],  # 6 blue
    ["#E2B6CF", "#E2B6CF"],  # 7 magenta
    ["#79A9D1", "#79A9D1"],  # 8 cyan
    ["#FDFFFC", "#FDFFFC"],  # 9 white
    ["#7A7D90", "#7A7D90"],  # 10 grey
    ["#FA8638", "#FA8638"],  # 11 orange
    ["#86E9CB", "#86E9CB"],  # 12 super cyan
    ["#30A3E0", "#30A3E0"],  # 13 super blue
    ["#242831", "#242831"],  # 14 super dark background
]


layout_theme = {
    "border_width": 2,
    "margin": 4,
    "border_focus": "30A3E0",
    "border_normal": "333D47",
    "font": "FiraCode Nerd Font",
    "grow_amount": 2,
}

layouts = [
    layout.Columns(**layout_theme, border_on_single=True,
        border_focus_stack="#30A3E0",
        border_normal_stack="#333D47"),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    layout.Spiral(**layout_theme, main_pane='left', clockwise=True, new_client_position='bottom'),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme),
]

# Setup bar

widget_defaults = dict(
    font="FiraCode Nerd Font",
    fontsize=15,
    padding=2,
    background=colors[0],
    decorations=[
        BorderDecoration(
            colour=colors[0],
            border_width=[13.50, 0, 12.50, 0],
        )
    ],
)

extension_defaults = widget_defaults.copy()

group_box_settings = {
    "padding": 4,
    "borderwidth": 1,
    "active": colors[9],
    "inactive": colors[10],
    "disable_drag": True,
    "rounded": True,
    "highlight_color": colors[2],
    "block_highlight_text_color": colors[6],
    "highlight_method": "block",
    "this_current_screen_border": colors[14],
    "this_screen_border": colors[7],
    "other_current_screen_border": colors[14],
    "other_screen_border": colors[14],
    "foreground": colors[1],
    "background": colors[14],
    "urgent_border": colors[3],
}

# Define functions for bar


def dunst():
    return subprocess.check_output(["./.config/qtile/dunst.sh"]).decode("utf-8").strip()


def toggle_dunst():
    qtile.cmd_spawn("./.config/qtile/dunst.sh --toggle")


def toggle_notif_center():
    qtile.cmd_spawn("./.config/qtile/dunst.sh --notif-center")


# Mouse_callback functions
def open_launcher():
    qtile.cmd_spawn("./.config/rofi/launchers/text/launcher.sh")


def kill_window():
    qtile.cmd_spawn("xdotool getwindowfocus windowkill")


def open_pavu():
    qtile.cmd_spawn("pavucontrol")
    

def open_powermenu():
    qtile.cmd_spawn("./.config/rofi/powermenu/powermenu.sh")


screens = [
    Screen(
        wallpaper="~/Pictures/Wallpapers/nasa.jpg",
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                widget.TextBox(
                    text="",
                    foreground=colors[13],
                    background=colors[0],
                    font="Font Awesome 6 Free Solid",
                    fontsize=26,
                    padding=10,
                    mouse_callbacks={"Button1": open_launcher},
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=24,
                    padding=0,
                ),
                widget.GroupBox(
                    font="Font Awesome 6 Brands",
                    visible_groups=[""],
                    **group_box_settings,
                ),
                widget.GroupBox(
                    font="Font Awesome 6 Free Solid",
                    visible_groups=["", "", "", "", "", "", "", "", ""],
                    **group_box_settings,
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=24,
                    padding=0,
                ),
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    background=colors[0],
                    padding=10,
                    size_percent=40,
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=24,
                    padding=0,
                ),
                widget.CurrentLayoutIcon(
                    custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
                    foreground=colors[2],
                    background=colors[14],
                    padding=-12,
                    scale=0.35,
                ),
                widget.WindowCount(
                    background=colors[14],
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=24,
                    padding=0,
                ),
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=10,
                    size_percent=50,
                ),
                
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=24,
                    padding=0,
                ),
                widget.TextBox(
                    text=" ",
                    foreground=colors[8],
                    background=colors[14],
                    font="Font Awesome 6 Free Solid",
                    # fontsize=38,
                ),
                widget.PulseVolume(
                    foreground=colors[8],
                    background=colors[14],
                    limit_max_volume="True",
                    mouse_callbacks={"Button1": open_pavu},
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=24,
                    padding=0,
                ),
                
                widget.Spacer(),
                widget.TextBox(
                    text=" ",
                    foreground=colors[12],
                    background=colors[0],
                    #fontsize=20,
                    font="Font Awesome 6 Free Solid",
                ),
                widget.WindowName(
                    background=colors[0],
                    foreground=colors[12],
                    width=bar.CALCULATED,
                    empty_group_string="Workstation",
                    max_chars=45,
                    mouse_callbacks={"Button2": kill_window},
                ),
                widget.Spacer(),
                widget.Systray(
                    icon_size=26,
                    background=colors[0],
                    padding=7,
                ),
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=10,
                    size_percent=50,
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=24,
                    padding=0,
                ),
                widget.GenPollText(
                    func=dunst,
                    update_interval=1,
                    foreground=colors[11],
                    background=colors[14],
                    padding=8,
                    mouse_callbacks={
                        "Button1": toggle_dunst,
                        "Button3": toggle_notif_center,
                    },
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=24,
                    padding=0,
                ),
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=10,
                    size_percent=50,
                ),          
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=24,
                    padding=0,
                ),
                widget.Battery(
                    foreground=colors[4],
                    background=colors[14],
                    charge_char="",
                    full_char="",
                    discharge_char="",
                    format= "{char} {percent:1.0%} [{hour:d}:{min:02d}]",
                    empty_char="¯\_(ツ)_/¯",                    
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=24,
                    padding=0,
                ),         
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=10,
                    size_percent=50,
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=24,
                    padding=0,
                ),
                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    foreground=colors[5],  # fontsize=38
                    background=colors[14],
                ),
                widget.Clock(
                    format="%a, %b %d",
                    background=colors[14],
                    foreground=colors[5],
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=24,
                    padding=0,
                ),
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=10,
                    size_percent=50,
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=24,
                    padding=0,
                ),
                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    foreground=colors[11],  # fontsize=38
                    background=colors[14],
                ),
                widget.Clock(
                    format="%I:%M %p",
                    foreground=colors[11],
                    background=colors[14],
                ),
                widget.TextBox(
                    text="",
                    foreground=colors[14],
                    background=colors[0],
                    fontsize=24,
                    padding=0,
                ),
                widget.TextBox(
                    text="⏻",
                    foreground=colors[13],
                    font="Font Awesome 6 Free Solid",
                    fontsize=28,
                    padding=10,
                    mouse_callbacks={"Button1": open_powermenu},
                ),
            ],
            56,
            margin=[0, 0, 8, 0],
            border_width=[0, 0, 2, 0],
            border_color="#3b4252",
        ),
        bottom=bar.Gap(4),
        left=bar.Gap(4),
        right=bar.Gap(4),        
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = "floating_only"
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
reconfigure_screens = True

# Startup scripts


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/autostart.sh"])
    
# Window swallowing ;)
@hook.subscribe.client_new
def _swallow(window):
    pid = window.window.get_net_wm_pid()
    ppid = psutil.Process(pid).ppid()
    cpids = {
        c.window.get_net_wm_pid(): wid for wid, c in window.qtile.windows_map.items()
    }
    for i in range(5):
        if not ppid:
            return
        if ppid in cpids:
            parent = window.qtile.windows_map.get(cpids[ppid])
            parent.minimized = True
            window.parent = parent
            return
        ppid = psutil.Process(ppid).ppid()


@hook.subscribe.client_killed
def _unswallow(window):
    if hasattr(window, "parent"):
        window.parent.minimized = False


# Go to group when app opens on matched group
@hook.subscribe.client_new
def modify_window(client):
    # if (client.window.get_wm_transient_for() or client.window.get_wm_type() in floating_types):
    #    client.floating = True

    for group in groups:  # follow on auto-move
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            targetgroup = client.qtile.groups_map[
                group.name
            ]  # there can be multiple instances of a group
            targetgroup.cmd_toscreen(toggle=False)
            break


# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
