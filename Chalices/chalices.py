from manim import *

class CupDropAnimation(Scene):

    def slide_pellet(self, pellet, times=2, run_time=2, neg=False, final_loc=1.5*RIGHT):
        # NOTE: Assumes 4 cups right now
        if not neg:
            direction = LEFT
            neg_direction = RIGHT
        else:
            direction = RIGHT
            neg_direction = LEFT
            
        for time in range(times):
            self.play(
                pellet.animate.move_to(5.5*direction + UP*3), # Same height back and forth
                rate_func=smooth,
                run_time=run_time
            )
            if (time==times-1): # Last slide end on desired cup
                # NOTE: HARDCODED RIGHT NOW
                self.play(
                    pellet.animate.move_to(final_loc + UP*3), # Same height back and forth
                    rate_func=smooth,
                    run_time=run_time
                )

            else:
                self.play(
                    pellet.animate.move_to(5.5*neg_direction + UP*3), # Same height back and forth
                    rate_func=smooth,
                    run_time=run_time
                )

    def create_glowing_pellet(self, color=WHITE):
        pellet = Dot(radius=0.15, color=color)
        pellet.set_fill(color, opacity=1)
        glow = Annulus(
            inner_radius=0.15,
            outer_radius=0.25,
            color=color
        ).set_opacity(0.3)
        glowing_pellet = VGroup(pellet, glow).move_to(UP*3)
        return glowing_pellet
    
    def create_and_drop_pellet(self, times=2, run_time=2, final_loc=1.5*RIGHT, wait=0.2, color=WHITE, neg=False):  
        # Move pellet back and forth above cups and drop
        glowing_pellet = self.create_glowing_pellet(color)
        self.slide_pellet(pellet=glowing_pellet, times=times, run_time=run_time, final_loc=final_loc, neg=neg)
        # Drop pellet
        self.play(
            glowing_pellet.animate.move_to(final_loc + DOWN*1.5), # Same height back and forth
            rate_func=rate_functions.ease_in_cubic,
            run_time=0.8
        )
        self.wait(wait)
        return glowing_pellet

    def gen_state(self, colors, count, scale, shift, poisoned, drank):  
        # Add cups
        state_cups = []
        for i in range(count):
            cup_svg = SVGMobject(r"C:\Users\evang\Desktop\Personal Projects\Manim\Chalices\cup-svgrepo-com.svg").set_z_index(2)
            cup_svg.set_color_by_gradient(colors[i], WHITE)
            
            state_cups.append(cup_svg)

        cups = VGroup(*state_cups)
        cups.arrange(RIGHT, buff=1.5)
        cups.scale(scale).move_to(shift)

        # Add skulls for poison
        poison_skulls = VGroup()
        for poison_cup in poisoned:
            skull_cross_bones = SVGMobject(r"C:\Users\evang\Desktop\Personal Projects\Manim\Chalices\Skull_and_crossbones_vector.svg").scale(0.4).set_z_index(3)
            skull_cross_bones = skull_cross_bones.set_color(WHITE).scale(scale)
            skull_cross_bones.set_stroke(width=2.5)  # Adjust the width value as needed

            skull_cross_bones.next_to(cups[poison_cup], DOWN, buff=0.2)
            skull_cross_bones.shift(LEFT * 0.2) # Shift slightly left to look better for my cup svgs
            poison_skulls.add(skull_cross_bones)

        # Get arrow pointing to drank cup
        arrow = Arrow(start=UP, end=DOWN, color=WHITE)
        arrow.scale(scale)
        arrow.next_to(cups[drank], UP, buff=0.1)  # Position the arrow above the circle
        arrow.shift(LEFT * 0.2)

        state = VGroup(cups, poison_skulls, arrow)
        return state

    def create_skull_cross_bones(self, final_loc, fade_in=True):
        # Create a skull symbol of svg
        skull_cross_bones = SVGMobject(r"C:\Users\evang\Desktop\Personal Projects\Manim\Chalices\Skull_and_crossbones_vector.svg").scale(0.4).set_z_index(3)
        skull_cross_bones = skull_cross_bones.set_color(WHITE)
        skull_cross_bones.set_stroke(width=2.5)  # Adjust the width value as needed

        skull_cross_bones.next_to(final_loc + 2*DOWN, DOWN, buff=0.2)
        skull_cross_bones.shift(LEFT * 0.2) # Shift slightly left to look better for my cup svgs
        self.wait(0.1)
        if (fade_in):
            self.play(FadeIn(skull_cross_bones))
        return skull_cross_bones
    
    def create_and_drop_pellet_with_skull(self, times=2, run_time=2, final_loc=1.5*RIGHT, wait=0.2, pellet_color=WHITE, neg=False):
        pellet = self.create_and_drop_pellet(times=times, run_time=run_time, final_loc=final_loc, wait=wait, 
                                             color=pellet_color, neg=neg)
        
        skull_cross_bones = self.create_skull_cross_bones(final_loc=final_loc)
        return pellet, skull_cross_bones


    def give_example(self, cups_horizontal_locations, indexes, pellet_colors=None):
        pellet_funcs = []
        if (pellet_colors==None):
            pellet_colors = [WHITE for _ in range(len(cups_horizontal_locations))]
        for idx, cup_index in enumerate(indexes):
            if cup_index%2:
                neg=True
            else:
                neg=False
            func = self.create_and_drop_pellet_with_skull(times=1, run_time=0.5, final_loc=cups_horizontal_locations[cup_index],
                                                          pellet_color=pellet_colors[idx], neg=neg)
            pellet_funcs.append(func)
            
        pellets_group = VGroup(
            *pellet_funcs
        )

        return pellets_group

        
    def construct(self):
        # TODO split this into different Scene objects
        # Create 2 cups spaces horizontally
        self.cups_list = []
        colors = [RED, BLUE]
        cups_horizontal_locations = [2*LEFT, 1.5*RIGHT]
        for i in range(2):
            cup_svg = SVGMobject(r"C:\Users\evang\Desktop\Personal Projects\Manim\Chalices\cup-svgrepo-com.svg").set_z_index(2)
            cup_svg.set_color_by_gradient(colors[i], WHITE)
            
            self.cups_list.append(cup_svg)

        cups = VGroup(*self.cups_list)
        cups.arrange(RIGHT, buff=1.5).shift(DOWN)

        # Animate Cup Example
        self.play(FadeIn(cups)) 
        self.wait(5)

        # Drop 1 pellets on the left
        pellets_group = self.give_example(cups_horizontal_locations, indexes=[0])
        self.play(FadeOut(pellets_group))
        self.wait(2)

        # Drop 1 pellete on the right
        pellets_group = self.give_example(cups_horizontal_locations, indexes=[1])
        self.play(FadeOut(pellets_group), FadeOut(cups))
        self.wait(2)

        # Create grid of possibilities
        state_cups = VGroup()
        state_cups.add(self.gen_state(colors=[RED, BLUE], count=2, scale=0.7, 
                                    shift=2*UP+3.5*LEFT, poisoned=[0], drank=0))
        state_cups.add(self.gen_state(colors=[RED, BLUE], count=2, scale=0.7,
                                    shift=2*DOWN+3.5*LEFT, poisoned=[1], drank=0))
        state_cups.add(self.gen_state(colors=[RED, BLUE], count=2, scale=0.7, 
                                    shift=2*UP+3.5*RIGHT, poisoned=[0], drank=1))
        state_cups.add(self.gen_state(colors=[RED, BLUE], count=2, scale=0.7, 
                                    shift=2*DOWN+3.5*RIGHT, poisoned=[1], drank=1))
        
        # Survival text
        survival_text = VGroup()
        survival_text.add(Text("Dead").scale(0.7).set_color(RED).move_to(LEFT*0.8 + UP*0.5))
        survival_text.add(Text("Alive").scale(0.7).set_color(WHITE).move_to(RIGHT*0.8 + UP*0.5))
        survival_text.add(Text("Alive").scale(0.7).set_color(WHITE).move_to(LEFT*0.8 + DOWN*0.5))
        survival_text.add(Text("Dead").scale(0.7).set_color(RED).move_to(RIGHT*0.8 + DOWN*0.5))

        # Add grid to 4 states
        vertical_line = Line(UP * 4, DOWN * 4, color=WHITE).set_stroke(width=5)
        horizontal_line = Line(LEFT * 7, RIGHT * 7, color=WHITE).set_stroke(width=5)
        grid = VGroup(vertical_line, horizontal_line)

        # Play an animation
        self.play(FadeIn(grid))
        self.play(FadeIn(state_cups))
        self.wait(5)
        self.play(FadeIn(survival_text))
        self.wait(2)
        self.play(FadeOut(grid, state_cups, survival_text))

        # Give example with 3 cups
        self.cups_list = []
        colors = [RED, BLUE, GREEN]
        for i in range(3):
            cup_svg = SVGMobject(r"C:\Users\evang\Desktop\Personal Projects\Manim\Chalices\cup-svgrepo-com.svg").set_z_index(2)
            cup_svg.set_color_by_gradient(colors[i], WHITE)
            self.cups_list.append(cup_svg)

        cups = VGroup(*self.cups_list)
        cups.arrange(RIGHT, buff=1.5).shift(DOWN)

        cups_horizontal_locations = [np.array([cup.get_x(), 0, 0])+0.1*LEFT for cup in cups]
        
        # Animate Cup Example
        self.play(FadeIn(cups)) 

        text = Text("For 3 cups, there will be two pellets").scale(0.5).shift(UP*2)
        self.play(FadeIn(text))
        pellets_group = self.give_example(cups_horizontal_locations, indexes=[0, 1])
        self.play(FadeOut(pellets_group), FadeOut(text))

        text = Text("The pellets could be dropped in the same cup.").scale(0.5).shift(UP*2)
        self.play(FadeIn(text))
        pellets_group = self.give_example(cups_horizontal_locations, indexes=[2, 2])
        self.play(FadeOut(pellets_group), FadeOut(text))

        text = Text("To calculate the probability of surviving, \n"
        "we need to consider the case where \n"
        "the poisoners poison different vs similar cups.").scale(0.5).shift(UP*2)
        self.play(FadeIn(text))
        self.wait(3)
        self.play(FadeOut(text))

        text = Text("First consider the chance of picking the same cup. \n"
                    "To do this, consider the first pellet to distinct from the second (by color).").scale(0.5).shift(UP*2)
        self.play(FadeIn(text))
        self.wait(3)
        self.play(FadeOut(text))
        text = Text("Given the first cup is poisoned, there is only one way for this to occur").scale(0.5).shift(UP*2)
        cup_0_skull_bones = self.create_skull_cross_bones(cups_horizontal_locations[0])
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

        pellets_groups = self.give_example(cups_horizontal_locations, indexes=[0, 0], pellet_colors=[RED_C, BLUE_C])
        self.wait(3)
        self.play(FadeOut(cup_0_skull_bones), FadeOut(pellets_groups))

        # Give example with colored pellet
        text = Text("If the first and second cup are poisoned, there are two ways for this to occur.").scale(0.5).shift(UP*2)
        cup_1_skull_bones = self.create_skull_cross_bones(cups_horizontal_locations[1], fade_in=False)
        self.play(FadeIn(text, cup_0_skull_bones, cup_1_skull_bones))
        self.wait(1)
        self.play(FadeOut(text))

        text = Text("Red in first cup, blue in second").scale(0.5).shift(UP*2)
        self.play(FadeIn(text))
        pellets_group = self.give_example(cups_horizontal_locations, indexes=[0, 1], pellet_colors=[RED, BLUE])
        self.play(FadeOut(text), FadeOut(pellets_group))

        text = Text("Red in second cup, blue in first").scale(0.5).shift(UP*2)
        self.play(FadeIn(text))
        pellets_group = self.give_example(cups_horizontal_locations, indexes=[1, 0], pellet_colors=[RED, BLUE])
        self.play(FadeOut(text, pellets_group, cup_0_skull_bones, cup_1_skull_bones))

        # Symmetry
        text = Text("To compute this probability, we can first arbitrarily select a cup to drink.").scale(0.5).shift(UP*2)
        # Create a surrounding rectangle with buffer
        cup_rect = SurroundingRectangle(cups[0], color=RED_D, buff=0.3)  # Adjust buff as needed
        self.play(FadeIn(text, cup_rect))
        self.wait(3)
        self.play(FadeOut(text))
        diagram = VGroup(cup_rect, cups)

        # Move cups to the side for reference
        self.play(diagram.animate.scale(0.5).move_to(RIGHT * 3))
        self.wait(3)    

        drinking_text = Text("How many ways are there to survive drinking from this cup?").scale(0.4).shift(UP*2 + LEFT*3)
        self.play(FadeIn(drinking_text))
        self.wait(2)

        # Get smaller pelllet locaitons
        p1 = self.create_glowing_pellet()
        p2 = self.create_glowing_pellet()

        p1.scale(0.6).move_to(UP*2 + RIGHT*2.5)
        p2.scale(0.6).move_to(UP*2 + RIGHT*3.5)

        brace_text = Brace(VGroup(cups[1], cups[2]), direction=DOWN)
        label_text = brace_text.get_text("Safe cups to drop pellets").scale(0.5)
        cups_text = Tex("$n=3$ cups").scale(0.7).next_to(cups, direction=DOWN).shift(DOWN*1.5)
        self.play(FadeIn(brace_text, label_text, cups_text))
        self.wait(2)

        # Display pellet possibilities
        p1_combos = [(p1.get_bottom(), cups[1].get_top()),
                     (p1.get_bottom(), cups[2].get_top())]
        p2_combos = [(p2.get_bottom(), cups[1].get_top()),
                    (p2.get_bottom(), cups[2].get_top())]
        
        p1_arrows = [Arrow(start=t[0], end=t[1], buff=0.2,            
                      stroke_color=WHITE,  # Set color to white
                      stroke_width=2,  # Make it thin for a lighter look
                      tip_length=0.1,
                    ) for t in p1_combos]
        
                
        p2_arrows = [Arrow(start=t[0], end=t[1], buff=0.2,            
                      stroke_color=WHITE,  # Set color to white
                      stroke_width=2,  # Make it thin for a lighter look
                      tip_length=0.1,
                    ) for t in p2_combos]
        
        self.play(FadeIn(p1, p2))
        self.play(FadeIn(VGroup(p1_arrows, p2_arrows)))
        self.wait(5)

        # Play the possibilities
        for p1_arrow in p1_arrows:
            for p2_arrow in p2_arrows:
                # Highlight specific arrows
                self.play(
                    p1_arrow.animate.set_stroke(color=RED, width=5),
                    p2_arrow.animate.set_stroke(color=BLUE, width=5), 
                    run_time=0.3,
                )

                # Unhighlight specific arrows          
                self.play(
                    p1_arrow.animate.set_stroke(color=WHITE, width=2),
                    p2_arrow.animate.set_stroke(color=WHITE, width=2), 
                    run_time=0.3,
                )

        # TODO could make a run algebra function for this instead of copying it down
        algebra = [
            Tex("$(3-1)^{3-1}$"),
            Tex("$(3-1)^{3-1}$"),
            Tex("$=2^{2}$"),
            Tex("$=4$"),
            Tex("$=4$"),
            Tex("$4 = (n-1)^{n-1}$")
        ]
        algebra[0].move_to(UP+LEFT*3)
        for idx in range(len(algebra[:-1])):
            algebra[idx+1].move_to(UP+LEFT*3)
            self.play(Transform(algebra[0], algebra[idx+1]), run_time=1)

        # Calculate the total possibilities 
        total_text = Text("How many ways are there total?").scale(0.4).shift(LEFT*3)

        # Get arrows for total possibilities
        p1_arrows.append(Arrow(start=p1.get_bottom(), end=cups[0].get_top(), buff=0.2,            
                        stroke_color=WHITE,  # Set color to white
                        stroke_width=2,  # Make it thin for a lighter look
                        tip_length=0.1,
                        ))
        p2_arrows.append(Arrow(start=p2.get_bottom(), end=cups[0].get_top(), buff=0.2,            
                        stroke_color=WHITE,  # Set color to white
                        stroke_width=2,  # Make it thin for a lighter look
                        tip_length=0.1,
                        ))
        
        self.play(FadeIn(total_text, p1_arrows[-1], p2_arrows[-1])) # Fade in new arrows with text
        self.wait(2)
        
        # Play the possibilities
        for p1_arrow in p1_arrows:
            for p2_arrow in p2_arrows:
                # Highlight specific arrows
                self.play(
                    p1_arrow.animate.set_stroke(color=RED, width=5),
                    p2_arrow.animate.set_stroke(color=BLUE, width=5), 
                    run_time=0.3,
                )

                # Unhighlight specific arrows          
                self.play(
                    p1_arrow.animate.set_stroke(color=WHITE, width=2),
                    p2_arrow.animate.set_stroke(color=WHITE, width=2), 
                    run_time=0.3,
                )

        algebra = [
            Tex("$3^{3-1}$"),
            Tex("$3^{3-1}$"),
            Tex("$=3^{2}$"),
            Tex("$=9$"),
            Tex("$=9$"),
            Tex("$9 = n^{n-1}$")
        ]
        algebra[0].move_to(DOWN+LEFT*3)
        for idx in range(len(algebra[:-1])):
            algebra[idx+1].move_to(DOWN+LEFT*3)
            self.play(Transform(algebra[0], algebra[idx+1]), run_time=1)

        # Fade out example on the side for result
        example_group = VGroup(p1_arrows, p2_arrows, cup_rect, brace_text, cups_text, cups_text, label_text, cups, p1, p2)
        self.play(FadeOut(example_group))

        # Expand to get the result
        eqns = MathTex(
            r"\frac{\text{Success}}{\text{Total}} = ", r"\frac{(n-1)^{n-1}}{n^{n-1}} ", "=", r"\frac{4}{9}"
        )   
        eqns.move_to(RIGHT*3)

        self.play(Write(eqns[0]), run_time=1)
        self.play(Write(eqns[1]), run_time=1)
        self.play(Write(eqns[2]), run_time=1)
        self.play(Write(eqns[3]), run_time=1)

        decimal_value = MathTex("0.44").move_to(eqns[3].get_center()).shift(RIGHT*0.1) # Nicer spacing this way
        approx = MathTex(r"\approx").move_to(eqns[2].get_center()).shift(LEFT*0.1)
        self.play(Transform(eqns[2], approx), Transform(eqns[3], decimal_value))

        self.wait(5)


        # Create 4 cups spaced horizontally
        if False:
            self.cups_list = []
            colors = [RED, BLUE, GREEN, YELLOW]
            cups_horizontal_locations = [5.5*LEFT, 2*LEFT, 1.5*RIGHT, 5*RIGHT]
            for i in range(4):
                cup_svg = SVGMobject(r"C:\Users\evang\Desktop\Personal Projects\Manim\Chalices\cup-svgrepo-com.svg").set_z_index(2)
                cup_svg.set_color_by_gradient(colors[i], WHITE)
                
                self.cups_list.append(cup_svg)

            cups = VGroup(*self.cups_list)
            cups.arrange(RIGHT, buff=1.5).shift(DOWN)
            
            # Animate Cup Example
            self.play(FadeIn(cups)) 

            pellets_group = self.give_example(cups_horizontal_locations, indexes=[0, 0, 1])
            self.play(FadeOut(pellets_group))

            pellets_group = VGroup(
                self.create_and_drop_pellet_with_skull(final_loc=cups_horizontal_locations[2]),
                self.create_and_drop_pellet_with_skull(times=1, run_time=0.5, final_loc=cups_horizontal_locations[1], neg=True),
                self.create_and_drop_pellet_with_skull(times=1, run_time=0.5, final_loc=cups_horizontal_locations[3]),
            )
            self.play(FadeOut(pellets_group))

            self.wait(1)


