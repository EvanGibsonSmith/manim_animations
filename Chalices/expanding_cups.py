from manim import *

class ExpandingCups(Scene):
    def construct(self):
        start_num = 4
        cup = SVGMobject("Chalices\cup-svgrepo-com.svg").scale(0.5)  # Placeholder SVG
        cups = VGroup(*[cup.copy() for _ in range(start_num)])
        cups.arrange(RIGHT, buff=0.5)
        cups.move_to(DOWN)
        
        pellets = []
        for _ in range(start_num-1):
            pellet = Dot(radius=0.15, color=WHITE)
            pellet.set_fill(WHITE, opacity=1)
            glow = Annulus(
                inner_radius=0.15,
                outer_radius=0.25,
                color=WHITE
            ).set_opacity(0.3)
            glowing_pellet = VGroup(pellet, glow)
            pellets.append(glowing_pellet)

        pellets = VGroup(*[pellet for pellet in pellets])
        pellets.arrange(RIGHT, buff=0.5)
        pellets.move_to(UP*2)
        
        self.play(FadeIn(cups), FadeIn(pellets))
        
        num_steps = 2  # Controls how long before cutting off
        
        for i in range(num_steps):
            new_cups = VGroup()
            new_pellets = VGroup()
            scale_factor = 0.8 # Shrinking factor per step
            spacing_factor = 0.1  # Controls packing
            pellet_scale_factor = 0.7  
            
            for cup in cups:
                for _ in range(2):  # Doubling cups
                    new_cup = cup.copy().scale(scale_factor)
                    new_cups.add(new_cup)
            
            # Create a corresponding number of pellets (num_cups - 1)
            num_pellets = len(new_cups) - 1
            for _ in range(num_pellets):
                pellet = Dot(radius=0.15 * pellet_scale_factor, color=WHITE)
                pellet.set_fill(WHITE, opacity=1)
                glow = Annulus(
                    inner_radius=0.15 * pellet_scale_factor,
                    outer_radius=0.25 * pellet_scale_factor,
                    color=WHITE
                ).set_opacity(0.3)
                glowing_pellet = VGroup(pellet, glow)
                new_pellets.add(glowing_pellet)
            
            new_cups.arrange(RIGHT, buff=spacing_factor)  # Expanding in a line
            new_cups.move_to(DOWN)
            
            # Adjust rows and columns dynamically for better packing
            num_rows = max(1, int(num_pellets // 4))  # Square root for better fit
            num_cols = max(1, (num_pellets + num_rows - 1) // num_rows + 2)  # Distribute evenly
            new_pellets.arrange_in_grid(rows=num_rows, cols=num_cols, buff=0.3)
            new_pellets.move_to(UP * 2)
            
            self.play(Transform(cups, new_cups), Transform(pellets, new_pellets), run_time=0.8/(i+1))  # Speed increases
        
        # Add ellipses at the ends to suggest continuation
        ellipsis_left_cups = MathTex("\dots").next_to(cups, LEFT, buff=0.5)
        ellipsis_right_cups = MathTex("\dots").next_to(cups, RIGHT, buff=0.5)
        ellipsis_left_pellets = MathTex("\dots").next_to(pellets, LEFT, buff=0.5)
        ellipsis_right_pellets = MathTex("\dots").next_to(pellets, RIGHT, buff=0.5)
        self.play(FadeIn(ellipsis_left_cups, ellipsis_right_cups), FadeIn(ellipsis_left_pellets, ellipsis_right_pellets))
        
        self.play(FadeOut(cups, new_pellets, 
                          ellipsis_left_cups, ellipsis_right_cups,
                          ellipsis_left_pellets, ellipsis_right_pellets))
