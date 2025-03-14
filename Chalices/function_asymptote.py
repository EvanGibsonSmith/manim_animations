from manim import *
import numpy as np
import math

class SurvivalGraphAndAlgebra(Scene):
    def construct(self):
        # Define the axes with custom tick frequency for y-axis
        axes = Axes(
            x_range=[1, 10], y_range=[0.3, 1, 0.1],
            axis_config={"color": BLUE, "include_numbers": True},
        )

        # Label the axes
        axes_labels = axes.get_axis_labels(x_label="n", y_label=Tex(r"$P[\text{Survival}]$"))
        
        def func(n):
            return ((n - 1)**(n - 1)) / (n**(n - 1))

        graph = axes.plot(lambda n: func(n), color=WHITE, x_range=[1, 10])
        func_tex = MathTex(r"\lim_{n \to \infty}", r"f[n]=", r"\lim_{n \to \infty}", r"\frac{(n-1)^{n-1}}{n^{n-1}}")
        func_tex.scale(1.5).move_to(UP*2)
        func_tex[3].shift(LEFT*1.7) # To make spacing nice before limit
        self.play(Create(axes), Write(axes_labels), Create(func_tex[1]), Create(func_tex[3]))
        self.play(Create(graph))

        scatter_points = VGroup()
        for i in range(2, 10):  # Generate points for n = 2 to 9
            scatter_points.add(Dot(point=axes.c2p(i, func(i)), color=YELLOW))

        ##self.play(FadeIn(scatter_points))
        for dot in scatter_points:
            self.play(FadeIn(dot), run_time=0.2)

        y_val = 1 / math.e
        horizontal_line = axes.plot(lambda y: y_val, x_range=[1, 10]) 
        horizontal_line.set_color(RED) 
        dashed_line = DashedVMobject(horizontal_line, num_dashes=20)  
        self.play(Create(dashed_line))
        
        label = Tex(r"?")  
        label.set_color(RED)
        label.move_to(axes.c2p(1, y_val) + RIGHT * 0.5 + UP * 0.5) 
        self.play(Write(label))
        
        self.wait(4)

        # Do the algebra on the function
        limit_text = Tex(r"What is this value as $n \to \infty$")
        self.play(
            Write(limit_text),
            Wiggle(label),
            Wiggle(dashed_line),
        )
        diagram_group = VGroup(label, dashed_line, scatter_points, graph, axes, axes_labels)
        self.play(FadeOut(diagram_group))
        self.play(Create(func_tex[0]), func_tex[3].animate.shift(RIGHT*1.7)) # Shift back to put limit in
        self.play(Create(func_tex[2]))

        self.wait(2)
        self.play(Unwrite(limit_text))


        # Do algebra to figure out answer
        eqns = MathTex(
            #r"\lim_{n \to \infty} f[n]=\lim_{n \to \infty} & = \frac{(n-1)^{n-1}}{n^{n-1}} \\ ",
            r"\lim_{n \to \infty} f[n] & = \lim_{n \to \infty} \left(\frac{n-1}{n}\right)^{n-1} \\",
            r"\lim_{n \to \infty} f[n] & = \lim_{n \to \infty} \frac{1}{\left(\frac{n}{n-1}\right)^{n-1}} \\",
            r"\lim_{n \to \infty} f[n] & = \lim_{(x-1) \to \infty} \frac{1}{\left(\frac{x+1}{(x+1)-1}\right)^{(x+1)-1}} \\",
            r"\lim_{n \to \infty} f[n] & = \lim_{x \to \infty} \frac{1}{\left(\frac{x+1}{x}\right)^{x}} \\",
            r"\lim_{n \to \infty} f[n] & = \lim_{x \to \infty} \frac{1}{\left(1+\frac{1}{x}\right)^{x}} \\",
            r"\lim_{n \to \infty} f[n] & = \frac{1}{\lim_{x \to \infty} \left(1+\frac{1}{x}\right)^{x}} \\",
            r"\lim_{n \to \infty} f[n] & = \frac{1}{e} \approx 0.368 \\",
        )
        eqns.shift(RIGHT*2 + DOWN*3)
        self.play(func_tex.animate.next_to(eqns[0], direction=UP).scale(2/3).shift(LEFT*0.2)) # Shift is to align =
        self.play(Write(eqns[0]))
        self.play(Write(eqns[1]))
        change_of_var_tex = Tex("Let $n=x+1$").next_to(eqns[2], direction=LEFT).shift(UP*0.2).scale(0.8).set_color(BLUE)
        self.play(Write(change_of_var_tex), Write(eqns[2]))
        up_amt = 3.2
        # Scroll up
        self.play(func_tex.animate.shift(UP*up_amt), 
                  eqns[0].animate.shift(UP*up_amt), # Shift visible ones
                  eqns[1].animate.shift(UP*up_amt),
                  eqns[2].animate.shift(UP*up_amt), 
                  change_of_var_tex.animate.shift(UP*up_amt)) # Shift up for more equations
        
        eqns[3].shift(UP*up_amt) # Shift currently hidden equations up as well
        eqns[4].shift(UP*up_amt)
        eqns[5].shift(UP*up_amt) 
        eqns[6].shift(UP*up_amt) 
        self.play(Write(eqns[3]))
        self.play(Write(eqns[4]))
        self.play(Write(eqns[5]))

        up_amt = 2
        self.play(eqns[:-1].animate.shift(UP*up_amt), # Move all visible eqns
                  change_of_var_tex.animate.shift(UP*up_amt))
        eqns[6].shift(UP*up_amt) 

        # Definition of e
        e_definition_tex = Tex(r"$e=\lim_{x \to \infty}\left(1+\frac{1}{x}\right)^{x}$").next_to(eqns[6], direction=LEFT, buff=0.1).scale(0.8).set_color(BLUE)
        self.play(Write(e_definition_tex))
        self.play(Write(eqns[6]))
        self.play(Wiggle(eqns[6]))
        self.wait(5)

