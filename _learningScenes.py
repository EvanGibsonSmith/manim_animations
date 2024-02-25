from manim import *

# for references
class GraphingScene(Scene):
    def construct(self):     
        axes = Axes(
            x_range = (0, 7),
            y_range = (0, 5),
            x_length = 7,
            axis_config={"include_numbers": True},
        )
        x_values = [0, 1.5, 2, 3, 4, 6.3]
        y_values = [1, 3, 2.5, 4, 2, 1.2]
        coords = [axes.c2p(x,y) for x,y in zip(x_values,y_values)]
        plot = VMobject(color=BLUE).set_points_as_corners(coords)

        self.add(axes,plot)

class SmallSignalGraphs(Scene):
    def construct(self):
        gateVoltageToSatCurrent = FunctionGraph(
            lambda t: t**2, # TODO get proper equation
            color=RED,
        ).move_to(LEFT*2 + UP*2)

        drainSourceVoltageToCurrent = FunctionGraph(
            lambda t: t, # TODO get proper equation
            color=BLUE,
        ).move_to(RIGHT*2 + UP*2)

        self.play(Write(gateVoltageToSatCurrent))
        self.play(Write(drainSourceVoltageToCurrent))


class GraphMovingExample(Scene):
    def construct(self):
        # value to move it up and down
        p = ValueTracker(1)

        def safe_func(x, func):
            out = func(x)
            if (np.isnan(out) or np.isinf(out)):
                return 0
            else:
                return out
            
        def update_graph1(mobject):
            mobject.become(FunctionGraph(lambda x: safe_func(x, lambda x: np.sin(x**(np.cos(p.get_value())))), x_range=[0, 10], color="RED"))

        def update_graph2(mobject):
            mobject.become(FunctionGraph(lambda x: safe_func(x, lambda x: np.cos(p.get_value())*np.cos(x-p.get_value())), x_range=[0, 10], color="BLUE"))

        axes = Axes(
            axis_config={"color": WHITE},
            y_range=(-5, 5, 1),
            x_range=(-10, 10, 1),
            x_length=10,
            tips=True,
        )
        self.add(axes)
        
        graphFunc1 = FunctionGraph(lambda x: x, color="RED", x_range=[0, 10])
        self.add(graphFunc1)
        graphFunc1.add_updater(update_function=update_graph1)

        graphFunc2= FunctionGraph(lambda x: x, color="BLUE", x_range=[0, 10])
        self.add(graphFunc2)
        graphFunc2.add_updater(update_function=update_graph2)

        self.play(
            ApplyMethod(p.increment_value,20),
            run_time=5,
        )

class SmallSignalGraphMoving(Scene):
    def construct(self):
        # value to move it up and down
        p = ValueTracker(0)

        def update_axes():
            newAxes = Axes(
                axis_config={"color": WHITE},
                #y_range=[graphFunc(np.linspace(0,10).argmin()), graphFunc(np.linspace(0,10)).argmax()],
                y_range=(0, 10, 1),
                x_range=(0, 20, 1),
                #x_axis_config={
                #    "numbers_to_include": np.arange(-10, 10.01, 2),
                #    "numbers_with_elongated_ticks": np.arange(-10, 10.01, 2),
                #},
                #tips=False,
            )
            newAxes.plot(lambda x: np.cos(x)*p.get_value())
            return newAxes

        def update_graph(axes):
            newAxes = update_axes()
            axes.become(newAxes)

        kWL = 1
        Vth = 0.4
        Vds = 5
        #graphFunc = lambda Vgs: kWL*((Vgs-Vth)*Vds-0.5*(Vds**2))

        axes = Axes(
            axis_config={"color": WHITE},
            #y_range=[graphFunc(np.linspace(0,10).argmin()), graphFunc(np.linspace(0,10)).argmax()],
            y_range=(3, 10, 1),
            x_range=(3, 20, 1),
            #x_axis_config={
            #    "numbers_to_include": np.arange(-10, 10.01, 2),
            #    "numbers_with_elongated_ticks": np.arange(-10, 10.01, 2),
            #},
            #tips=False,
        )
        axes.plot(lambda x: x**2)
        self.add(axes)
        
        # fix TODO skWL*((Vgs-Vth)*Vds-0.5*(Vds**2))
        #gateVoltageToSatCurrent = axes.plot(graphFunc, color=BLUE)

        """drainSourceVoltageToCurrent = FunctionGraph(
            lambda t: t, # TODO get proper equation
            color=BLUE,
        ).move_to(RIGHT*2 + UP*2)"""

        #self.add(gateVoltageToSatCurrent)
        self.play(
            ApplyMethod(p.increment_value,0.01),
            run_time=5,
        )
        
class NextToUpdater(Scene):
    def construct(self):
        def dot_position(mobject):
            mobject.set_value(dot.get_center()[0])
            mobject.next_to(dot)

        dot = Dot(RIGHT*3)
        label = DecimalNumber()
        label.add_updater(dot_position)
        self.add(dot, label)

        self.play(Rotating(dot, about_point=ORIGIN, angle=TAU, run_time=TAU, rate_func=linear))
        #self.play(Write(drainSourceVoltageToCurrent))

class PlotTwoGraphsAtOnce(GraphingScene):
    CONFIG = {
        "y_max" : 40,
        "y_min" : 0,
        "x_max" : 7,
        "x_min" : 0,
        "y_tick_frequency" : 10,
        "x_tick_frequency" : 1,
        "x_axis_width": 6,
        "y_axis_height": 3,
        "axes_color" : GRAY, 
    }
    def construct(self):
         
        self.graph_origin = -0.5 * DOWN + 3 * LEFT
        self.setup_axes(animate=True)
        graph_up = self.get_graph(lambda x : x**2, 
                                    color = GOLD_A,
                                    x_min = 0, 
                                    x_max = 3
                                    )
        f1 = Tex(r"f(x) = {x}^2", color = GOLD_A)
        f1.scale(0.7)
        label_coord1 = self.input_to_graph_point(3,graph_up)
        f1.next_to(label_coord1,RIGHT+UP)
        self.graph_origin = 3.5 * DOWN + 3 * LEFT
        self.setup_axes(animate=True)
        graph_down = self.get_graph(lambda x : x**3, 
                                    color = BLUE_D,
                                    x_min = 0, 
                                    x_max = 3
                                    )
        graphs=VGroup(graph_up,graph_down)
        f2 = Tex(r"f(x) = {x}^3", color = BLUE_D)
        f2.scale(0.7)
        label_coord2 = self.input_to_graph_point(3,graph_up)
        f2.next_to(label_coord2,RIGHT+UP)
        self.play(
            Create(graphs),
            run_time = 2,
        )
        self.play(Create(f1), Create(f2))
        self.wait(3)

class MyTwoGraphsAtOnce(Scene):
    def construct(self):
        ax1 = Axes(
            x_range=[0, 10, 1],
            y_range=[-5, 5, 1],
            tips=StealthTip,
            axis_config={"include_numbers": True, "color": RED},
            x_length=5,
            y_length=5,
        )
        ax1.move_to(LEFT*3)

        ax2 = Axes(
            x_range=[0, 10, 1],
            y_range=[-5, 5, 1],
            tips=StealthTip,
            axis_config={"include_numbers": True, "color": BLUE},
            x_length=5,
            y_length=5,
        )
        ax2.move_to(RIGHT*3)

        # write axes
        self.play(Write(ax1), Write(ax2))

        # write curve for each
        self.play(Write(ax1.plot(lambda x: np.sin(x), color=YELLOW)), run_time=3)

        self.play(Write(ax2.plot(lambda x: np.cos(x), color=YELLOW)), run_time=3)

        self.wait(2)


class MOSFETGraphs(Scene):
    def construct(self):
        # set parameters
        kPrimeWL = 1
        Vth = 0.4
        Vgs = 3
        
        # derived params
        Vod = Vgs - Vth
        
        def DrainSourceToCurrent(Vds):
            if (Vds<Vod): # less than overdrive, use triode equation
                return kPrimeWL*(Vod*Vds-0.5*(Vds**2))
            else: # in SAT region
                return 0.5*kPrimeWL*((Vod)**2) # no lambda for now
            
        def GateSourceToSatCurrent(Vgs):
            if (Vgs<Vth):
                return 0
            else:
                return 0.5*kPrimeWL*((Vgs-Vth)**2) # no lambda for now

        
        ax1 = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 5, 1],
            tips=False,
            axis_config={"include_numbers": True, "color": WHITE},
            x_length=5,
            y_length=5,
        )
        ax1.move_to(LEFT*3)

        # graphing parameters
        headroom = 0.1 # how much above the max at sat to show as a multiplier
        # get range of drain to source with params to plot properly
        satValue = 0.5*kPrimeWL*((Vod)**2)
        ax2 = Axes(
            x_range=[0, 10], # TODO set numbers
            y_range=[0, satValue*(1+headroom)],
            tips=False,
            axis_config={"include_numbers": True, "color": WHITE},
            x_length=5,
            y_length=5,
        )
        ax2.move_to(RIGHT*3)

        # write axes
        self.play(Write(ax1), Write(ax2))
        self.play(Write(ax1.plot(GateSourceToSatCurrent, x_range=[0, 3], color=WHITE), run_time=3))

        # write curve for each
        self.play(Write(ax2.plot(DrainSourceToCurrent, color=WHITE)), 
                  run_time=3)

        # make divider/brace for this region
        satValue = DrainSourceToCurrent(Vod)
        linSatPoint = ax2.coords_to_point(Vod, satValue)
        linSatRegionDividerLine = ax2.get_vertical_line(linSatPoint, line_config={"dashed_ratio": 0.85}, color=YELLOW)

        linRegionLeftPoint = ax2.coords_to_point(0, satValue)
        linearRegionBrace = BraceBetweenPoints(linRegionLeftPoint, linSatPoint, UP, color=RED_B)
        linearRegionBraceText = linearRegionBrace.get_text("LIN")

        satRegionRightPoint = ax2.coords_to_point(10, satValue) # TODO using 10 as end of the graph
        satRegionBrace = BraceBetweenPoints(linSatPoint, satRegionRightPoint, UP, color=GREEN_B)
        satRegionBraceText = satRegionBrace.get_text("SAT")
        
        # add braces for the linear and saturation regions
        self.play(
            Write(linSatRegionDividerLine), 
            Write(linearRegionBrace),
            Write(linearRegionBraceText),
            Write(satRegionBrace),
            Write(satRegionBraceText),
        )

        gateSourceBraceHeight = GateSourceToSatCurrent(3) # TODO magic number 3 representing x range limit for graph
        onOffPoint = ax1.coords_to_point(Vth, gateSourceBraceHeight)
        
        onOffDividerLine = ax1.get_vertical_line(onOffPoint, line_config={"dashed_ratio": 0.85}, color=YELLOW)

        offRegionLeftPoint = ax1.coords_to_point(0, gateSourceBraceHeight)
        offRegionBrace = BraceBetweenPoints(offRegionLeftPoint, onOffPoint, UP, color=RED_B)
        offRegionBraceText = offRegionBrace.get_text("OFF")

        onRegionRightPoint = ax1.coords_to_point(3, gateSourceBraceHeight)
        onRegionBrace = BraceBetweenPoints(onOffPoint, onRegionRightPoint, UP, color=GREEN_B)
        onRegionBraceText = onRegionBrace.get_text("ON")

        self.play(
            Write(onOffDividerLine),
            # TODO off region looks bad not displayed right now
            #Write(offRegionBrace),
            #Write(offRegionBraceText),
            Write(onRegionBrace),
            Write(onRegionBraceText)
        )
        
        self.wait()
