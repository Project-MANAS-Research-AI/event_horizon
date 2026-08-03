"""Render the simple plasma-containment animation used by the README.

Run from the repository root with:

    uv run --group animation manim -r 600,338 --fps 8 --format=gif \
        animations/event_horizon_intro.py EventHorizonIntro
"""

import numpy as np
from manim import (
    BLACK,
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    WHITE,
    Circle,
    Create,
    DashedVMobject,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Scene,
    Text,
    Transform,
    VGroup,
    Wiggle,
    there_and_back,
)


BACKGROUND = "#07111F"
WALL = "#101D2B"
FLOOR = "#09121C"
METAL = "#66788A"
CYAN = "#42E8FF"
BLUE = "#2979FF"
PINK = "#FF4F9A"
MAGENTA = "#D82BFF"
ORANGE = "#FF9D45"
RED = "#FF334D"
SKIN = "#DDAA84"
SHIRT = "#5F7CF4"
YELLOW = "#FFD740"


def organic_shape(radius, phase, color, opacity, stroke_width=0, chaos=1.0):
    """Create a smooth-looking asymmetric plasma layer."""
    points = []
    for theta in np.linspace(0, 2 * PI, 96, endpoint=False):
        ripple = chaos * (
            0.12 * np.sin(5 * theta + phase)
            + 0.055 * np.sin(3 * theta - phase)
            + 0.025 * np.cos(7 * theta)
        )
        current_radius = radius * (1 + ripple)
        points.append(
            np.array(
                [
                    current_radius * np.cos(theta),
                    current_radius * np.sin(theta),
                    0,
                ]
            )
        )
    return Polygon(
        *points,
        fill_color=color,
        fill_opacity=opacity,
        stroke_color=color,
        stroke_width=stroke_width,
    )


def make_plasma(state="initial"):
    """Build the growing, unstable, or contained plasma state."""
    if state == "unstable":
        layers = (
            (1.62, 1.1, "#8A102C", 0.09, 0, 1.5),
            (1.45, 2.0, RED, 0.2, 0, 1.55),
            (1.22, 0.1, RED, 0.94, 5, 1.7),
            (0.69, 1.4, "#FF593D", 0.82, 0, 1.35),
            (0.32, 0.5, "#FFD3B8", 0.9, 0, 1.1),
        )
    elif state == "stable":
        layers = (
            (0.86, 0.3, BLUE, 0.07, 0, 0.65),
            (0.74, 1.2, CYAN, 0.15, 0, 0.65),
            (0.61, 0.7, "#328DFF", 0.94, 4, 0.7),
            (0.36, 1.7, CYAN, 0.78, 0, 0.6),
            (0.18, 0.2, WHITE, 0.9, 0, 0.55),
        )
    else:
        layers = (
            (1.08, 0.3, MAGENTA, 0.06, 0, 1.0),
            (0.94, 1.2, PINK, 0.14, 0, 1.0),
            (0.78, 0.7, PINK, 0.92, 4, 1.0),
            (0.48, 1.7, ORANGE, 0.75, 0, 1.0),
            (0.25, 0.2, WHITE, 0.8, 0, 1.0),
        )

    plasma_layers = [
        organic_shape(
            radius,
            phase,
            color,
            opacity,
            stroke_width=stroke_width,
            chaos=chaos,
        )
        for radius, phase, color, opacity, stroke_width, chaos in layers
    ]
    plasma = VGroup(*plasma_layers)
    plasma.move_to(LEFT * 0.75 + UP * 0.18)
    return plasma


def make_mouth(center, mood="neutral"):
    """Create a two-segment mouth that can morph between expressions."""
    if mood == "frown":
        left = center + LEFT * 0.08 + DOWN * 0.025
        middle = center + UP * 0.045
        right = center + RIGHT * 0.08 + DOWN * 0.025
    elif mood == "smile":
        left = center + LEFT * 0.08 + UP * 0.025
        middle = center + DOWN * 0.045
        right = center + RIGHT * 0.08 + UP * 0.025
    else:
        left = center + LEFT * 0.08
        middle = center
        right = center + RIGHT * 0.08
    return VGroup(
        Line(left, middle, color=BLACK, stroke_width=3),
        Line(middle, right, color=BLACK, stroke_width=3),
    )


def make_operator():
    """Build a small side-view operator seated at a computer."""
    desk = VGroup(
        RoundedRectangle(
            width=3.45,
            height=0.16,
            corner_radius=0.05,
            fill_color=METAL,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(RIGHT * 4.55 + DOWN * 1.42),
        Line([3.15, -1.48, 0], [3.15, -2.55, 0], color=METAL, stroke_width=8),
        Line([5.95, -1.48, 0], [5.95, -2.55, 0], color=METAL, stroke_width=8),
    )

    monitor_shell = RoundedRectangle(
        width=1.48,
        height=1.04,
        corner_radius=0.1,
        fill_color="#26384A",
        fill_opacity=1,
        stroke_color=METAL,
        stroke_width=4,
    ).move_to(RIGHT * 3.45 + DOWN * 0.72)
    screen = RoundedRectangle(
        width=1.16,
        height=0.72,
        corner_radius=0.06,
        fill_color="#071926",
        fill_opacity=1,
        stroke_color=CYAN,
        stroke_opacity=0.35,
        stroke_width=2,
    ).move_to(monitor_shell)
    monitor_stand = VGroup(
        Line([3.45, -1.24, 0], [3.45, -1.39, 0], color=METAL, stroke_width=6),
        Line([3.2, -1.4, 0], [3.7, -1.4, 0], color=METAL, stroke_width=6),
    )
    keyboard = RoundedRectangle(
        width=1.15,
        height=0.2,
        corner_radius=0.05,
        fill_color="#34495E",
        fill_opacity=1,
        stroke_color=METAL,
        stroke_width=2,
    ).move_to(RIGHT * 4.22 + DOWN * 1.28)

    chair = VGroup(
        RoundedRectangle(
            width=0.5,
            height=0.95,
            corner_radius=0.12,
            fill_color="#29394B",
            fill_opacity=1,
            stroke_color=METAL,
            stroke_width=3,
        ).move_to(RIGHT * 5.28 + DOWN * 1.43),
        Line([5.28, -1.9, 0], [5.28, -2.36, 0], color=METAL, stroke_width=7),
        Line([4.98, -2.38, 0], [5.58, -2.38, 0], color=METAL, stroke_width=5),
    )

    torso = RoundedRectangle(
        width=0.68,
        height=1.05,
        corner_radius=0.18,
        fill_color=SHIRT,
        fill_opacity=1,
        stroke_width=0,
    ).move_to(RIGHT * 5.05 + DOWN * 1.17)
    neck = Line([4.82, -0.77, 0], [4.76, -0.62, 0], color=SKIN, stroke_width=12)
    head = Circle(
        radius=0.34,
        fill_color=SKIN,
        fill_opacity=1,
        stroke_width=0,
    ).move_to(RIGHT * 4.72 + DOWN * 0.42)
    hair = Circle(
        radius=0.35,
        fill_color="#1C2230",
        fill_opacity=1,
        stroke_width=0,
    ).move_to(head.get_center() + RIGHT * 0.08 + UP * 0.08)
    face = Circle(
        radius=0.29,
        fill_color=SKIN,
        fill_opacity=1,
        stroke_width=0,
    ).move_to(head.get_center() + LEFT * 0.07 + DOWN * 0.015)
    eye = Dot(face.get_center() + LEFT * 0.2 + UP * 0.05, radius=0.035, color=BLACK)
    mouth = make_mouth(face.get_center() + LEFT * 0.11 + DOWN * 0.15)
    nose = Polygon(
        face.get_center() + LEFT * 0.29 + UP * 0.01,
        face.get_center() + LEFT * 0.4 + DOWN * 0.05,
        face.get_center() + LEFT * 0.27 + DOWN * 0.08,
        fill_color=SKIN,
        fill_opacity=1,
        stroke_width=0,
    )

    upper_arm_a = Line([4.76, -0.92, 0], [4.45, -1.13, 0], color=SHIRT, stroke_width=12)
    forearm_a = Line([4.45, -1.13, 0], [4.05, -1.2, 0], color=SKIN, stroke_width=9)
    hand_a = Dot([4.02, -1.22, 0], radius=0.075, color=SKIN)
    typing_arm_a = VGroup(upper_arm_a, forearm_a, hand_a)

    upper_arm_b = Line([4.88, -1.0, 0], [4.62, -1.22, 0], color=SHIRT, stroke_width=12)
    forearm_b = Line([4.62, -1.22, 0], [4.32, -1.28, 0], color=SKIN, stroke_width=9)
    hand_b = Dot([4.29, -1.29, 0], radius=0.075, color=SKIN)
    typing_arm_b = VGroup(upper_arm_b, forearm_b, hand_b)

    legs = VGroup(
        Line([5.0, -1.58, 0], [4.72, -2.0, 0], color="#26324C", stroke_width=15),
        Line([4.72, -2.0, 0], [4.14, -2.02, 0], color="#26324C", stroke_width=13),
    )

    code_lines = VGroup(
        Line([3.12, -0.58, 0], [3.65, -0.58, 0], color=CYAN, stroke_width=3),
        Line([3.12, -0.75, 0], [3.78, -0.75, 0], color=CYAN, stroke_width=3),
        Line([3.12, -0.92, 0], [3.52, -0.92, 0], color=CYAN, stroke_width=3),
    )

    operator = VGroup(
        desk,
        monitor_stand,
        monitor_shell,
        screen,
        keyboard,
        chair,
        legs,
        torso,
        neck,
        hair,
        face,
        eye,
        mouth,
        nose,
        typing_arm_a,
        typing_arm_b,
    )
    return operator, screen, code_lines, typing_arm_a, typing_arm_b, mouth


class EventHorizonIntro(Scene):
    """A growing plasma blob is stabilized by a computer-controlled boundary."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        back_wall = Rectangle(
            width=14.3,
            height=8.1,
            fill_color=WALL,
            fill_opacity=1,
            stroke_width=0,
        )
        wall_panels = VGroup(
            *[
                Line([-7.1, y, 0], [7.1, y, 0], color="#1B2B3B", stroke_width=2)
                for y in (-1.8, 0.55, 2.9)
            ],
            *[
                Line([x, -1.8, 0], [x, 4.0, 0], color="#1B2B3B", stroke_width=2)
                for x in (-4.8, 1.8, 6.2)
            ],
        )
        floor = Rectangle(
            width=14.3,
            height=2.3,
            fill_color=FLOOR,
            fill_opacity=1,
            stroke_width=0,
        ).to_edge(DOWN, buff=0)
        floor_edge = Line([-7.1, -2.15, 0], [7.1, -2.15, 0], color=METAL, stroke_width=3)

        plasma = make_plasma()
        unstable_plasma = make_plasma("unstable")
        stable_plasma = make_plasma("stable")
        operator, screen, code_lines, arm_a, arm_b, mouth = make_operator()
        frown = make_mouth(mouth.get_center(), "frown")
        smile = make_mouth(mouth.get_center(), "smile")
        reaction = Text("!?", font_size=34, weight="BOLD", color=YELLOW)
        reaction.move_to(RIGHT * 4.72 + UP * 0.32).rotate(-0.08)

        self.add(back_wall, wall_panels, floor, floor_edge)
        self.play(
            FadeIn(operator, shift=LEFT * 0.12),
            FadeIn(plasma, scale=0.65),
            run_time=0.65,
        )

        self.play(
            Transform(plasma, unstable_plasma),
            Transform(mouth, frown),
            FadeIn(reaction, shift=UP * 0.12),
            run_time=1.45,
            rate_func=lambda t: t * t * (3 - 2 * t),
        )
        self.play(
            Wiggle(
                plasma,
                scale_value=1.06,
                rotation_angle=0.09 * PI,
                n_wiggles=3,
            ),
            Wiggle(reaction, scale_value=1.12, rotation_angle=0.08 * PI),
            run_time=0.42,
        )

        self.play(
            arm_a.animate.shift(DOWN * 0.055),
            arm_b.animate.shift(UP * 0.045),
            screen.animate.set_fill(BLUE, opacity=0.26).set_stroke(CYAN, opacity=1),
            run_time=0.14,
        )
        self.play(
            arm_a.animate.shift(UP * 0.055),
            arm_b.animate.shift(DOWN * 0.045),
            FadeIn(code_lines[0]),
            run_time=0.14,
        )
        self.play(
            arm_a.animate.shift(DOWN * 0.055),
            arm_b.animate.shift(UP * 0.045),
            FadeIn(code_lines[1]),
            run_time=0.14,
        )
        self.play(
            arm_a.animate.shift(UP * 0.055),
            arm_b.animate.shift(DOWN * 0.045),
            FadeIn(code_lines[2]),
            run_time=0.14,
        )

        field_center = plasma.get_center()
        field_glow = Circle(
            radius=2.28,
            fill_color=CYAN,
            fill_opacity=0.035,
            stroke_color=CYAN,
            stroke_opacity=0.18,
            stroke_width=15,
        ).move_to(field_center)
        boundary = Circle(
            radius=2.16,
            color=CYAN,
            stroke_width=5,
        ).move_to(field_center)
        inner_boundary = DashedVMobject(
            Circle(radius=2.02, color=BLUE, stroke_width=3).move_to(field_center),
            num_dashes=42,
        )

        self.play(
            FadeIn(field_glow, scale=1.08),
            Create(boundary),
            Create(inner_boundary),
            Transform(mouth, smile),
            FadeOut(reaction, shift=UP * 0.1),
            run_time=0.62,
        )
        self.play(
            boundary.animate.scale(0.78),
            inner_boundary.animate.scale(0.78),
            field_glow.animate.scale(0.78).set_fill(CYAN, opacity=0.09),
            Transform(plasma, stable_plasma),
            run_time=1.35,
            rate_func=lambda t: t * t * (3 - 2 * t),
        )
        self.play(
            plasma.animate.scale(1.08),
            boundary.animate.set_stroke(opacity=0.75),
            inner_boundary.animate.set_stroke(opacity=0.55),
            rate_func=there_and_back,
            run_time=0.75,
        )
        self.wait(0.45)
