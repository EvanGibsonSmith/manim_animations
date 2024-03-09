from manim import *

class MOSFETGraphs(Scene):
    def construct(self):
        # set parameters
        kPrimeWL = 0.1
        Vth = 0.4
        VgsOperatingVoltage = 2 # TODO this does not have dependence on Vds as it actually does yet = 3
        
        # derived params
        Vod = VgsOperatingVoltage - Vth
        
        def DrainSourceToCurrent(Vds):
            # if off return 0
            if (Vod<0): # if off return zero
                return 0
            if (Vds<Vod): # less than overdrive, use triode equation
                return kPrimeWL*(Vod*Vds-0.5*(Vds**2))
            else: # in SAT region
                return 0.5*kPrimeWL*((Vod)**2) # no lambda for now
            
        def GateSourceToSatCurrent(Vgs):
            if (Vgs<Vth):
                return 0
            else:
                return 0.5*kPrimeWL*((Vgs-Vth)**2) # no lambda for now

        headroom = 0.1 # how much above the max at sat to show as a multiplier
        ax1 = Axes(
            x_range=[0, 3, 1],
            y_range=[0, GateSourceToSatCurrent(3)*(1+headroom), 1],
            tips=False,
            axis_config={"include_numbers": True, "color": WHITE},
            x_length=5,
            y_length=5,
        )
        ax1.move_to(LEFT*3)

        # graphing parameters
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
            Write(offRegionBrace),
            Write(offRegionBraceText),
            Write(onRegionBrace),
            Write(onRegionBraceText)
        )
        
        self.wait(1)

        # TODO when doign small signal analysis and moving vertical point and dot around together use a VGroup?
        # add operating region dots to the scene
        VdsOperatingVoltage = 4 # TODO put at top cause arbitrary choice
        VdsOperatingPoint = ax2.coords_to_point(VdsOperatingVoltage, DrainSourceToCurrent(VdsOperatingVoltage)) # TODO organize these param numbers
        VdsOperatingPointLine = ax2.get_vertical_line(VdsOperatingPoint, color=BLUE)
        self.play(Write(Dot(VdsOperatingPoint, color=BLUE)), Write(VdsOperatingPointLine))

        # Vgs operating point voltage is defined at the top
        VgsOperatingPoint = ax1.coords_to_point(VgsOperatingVoltage, GateSourceToSatCurrent(VgsOperatingVoltage)) # TODO organize these param numbers
        VgsOperatingPointLine = ax1.get_vertical_line(VgsOperatingPoint, color=BLUE)

        self.play(Write(VgsOperatingPointLine))
        self.play(Write(Dot(VgsOperatingPoint, color=BLUE)))


        self.wait(5)

class MOSFETGraphsSmallSignal(Scene):
    def construct(self):
        # set up time 
        simTime = ValueTracker(0)

        # set parameters
        kPrimeWL = 1
        Vth = 1
        
        # set parameters that are functions
        Vds = lambda t: 4 # constant for the moment # TODO this is done with the operating voltage right now
        Vgs = lambda t: 2 + 0.05*np.sin(t) # TODO this does not have dependence on Vds as it actually does yet = 3
        
        # derived params
        Vod = lambda t: Vgs(t) - Vth
        
        def DrainSourceToCurrent(Vds, t):
            if (Vod(t)<0): # if off return zero
                return 0
            if (Vds<Vod(t)): # less than overdrive, use triode equation
                return kPrimeWL*(Vod(t)*Vds-0.5*(Vds**2))
            else: # in SAT region
                return 0.5*kPrimeWL*((Vod(t))**2) # no lambda for now
            
        def GateSourceToSatCurrent(Vgs):
            if (Vgs<Vth):
                return 0
            else:
                return 0.5*kPrimeWL*((Vgs-Vth)**2)# no lambda for now

        headroom = 0.1 # how much above the max at sat to show as a multiplier
        ax1 = Axes(
            x_range=[0, 3, 1],
            y_range=[0, GateSourceToSatCurrent(3)*(1+headroom), 1],
            tips=False,
            axis_config={"include_numbers": True, "color": WHITE},
            x_length=5,
            y_length=5,
        )
        ax1.move_to(LEFT*3)
      
        # graphing parameters
        # get range of drain to source with params to plot properly
        satValue = 0.5*kPrimeWL*((Vod(0))**2)
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
        
        # TODO add stuff below
        gateSourceGraph = ax1.plot(lambda Vgs: GateSourceToSatCurrent(Vgs), x_range=[0, 3], color=WHITE)
        self.play(Write(gateSourceGraph), run_time=3)

        # write curve for each
        drainSourceGraph = ax2.plot(lambda Vds: DrainSourceToCurrent(Vds, simTime.get_value()), color=WHITE)
        self.play(Write(drainSourceGraph), run_time=3)

        # make divider/brace for this region. For the braces just use function values at time 0,
        # because they will be removed before simTime starts going
        satValue = DrainSourceToCurrent(Vod(0), 0)
        linSatPoint = ax2.coords_to_point(Vod(0), satValue)
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
            Write(offRegionBrace),
            Write(offRegionBraceText),
            Write(onRegionBrace),
            Write(onRegionBraceText)
        )
        
        self.wait(4) 
        # remove braces 
        self.play(
            Unwrite(linSatRegionDividerLine), 
            Unwrite(linearRegionBrace),
            Unwrite(linearRegionBraceText),
            Unwrite(satRegionBrace),
            Unwrite(satRegionBraceText),
            Unwrite(onOffDividerLine), # TODO make group for this stuff? this is too much
            Unwrite(offRegionBrace),
            Unwrite(offRegionBraceText),
            Unwrite(onRegionBrace),
            Unwrite(onRegionBraceText)
        )

        # TODO when doign small signal analysis and moving vertical point and dot around together use a VGroup?
        # add operating region dots to the scene
        # Vds shouldn't really vary, but if it does it is set up to be a function here
        # TODO double use of simTime.get_value in DrainSourceToCurrent is bad
        VdsOperatingPoint = ax2.coords_to_point(Vds(simTime.get_value()), DrainSourceToCurrent(Vds(simTime.get_value()), simTime.get_value())) # TODO organize these param numbers
        VdsOperatingPointLine = ax2.get_vertical_line(VdsOperatingPoint, color=BLUE)
        VdsOperationPointDot = Dot(VdsOperatingPoint, color=BLUE)

        # updaters to move this dot up and down (and left and right if needed)
        def updateVdsOperatingPointLine(line):
            newVdsOperatingPoint = ax2.coords_to_point(Vds(simTime.get_value()), DrainSourceToCurrent(Vds(simTime.get_value()), simTime.get_value())) # TODO organize these param numbers
            newVdsOperatingPointLine = ax2.get_vertical_line(newVdsOperatingPoint, color=BLUE)
            line.become(newVdsOperatingPointLine)

        def updateVdsOperatingPointDot(dot):
            newVdsOperatingPoint = ax2.coords_to_point(Vds(simTime.get_value()), DrainSourceToCurrent(Vds(simTime.get_value()), simTime.get_value())) # TODO organize these param numbers
            newVdsOperationPointDot = Dot(newVdsOperatingPoint, color=BLUE)
            dot.become(newVdsOperationPointDot)

        VdsOperatingPointLine.add_updater(updateVdsOperatingPointLine)
        VdsOperationPointDot.add_updater(updateVdsOperatingPointDot)

        # create dot for Vgs and move it with function given
        # Vgs operating point voltage is defined at the top
        VgsOperatingPoint = ax1.coords_to_point(Vgs(simTime.get_value()), GateSourceToSatCurrent(Vgs(simTime.get_value()))) # TODO organize these param numbers
        VgsOperatingPointLine = ax1.get_vertical_line(VgsOperatingPoint, color=BLUE)
        VgsOperatingPointDot = Dot(VgsOperatingPoint, color=BLUE)

        def updateVgsOperatingPointLine(line):
            newVgsOperatingPoint = ax1.coords_to_point(Vgs(simTime.get_value()), GateSourceToSatCurrent(Vgs(simTime.get_value())))
            newVgsOperatingPointLine = ax1.get_vertical_line(newVgsOperatingPoint, color=BLUE)
            line.become(newVgsOperatingPointLine)

        def updateVgsOperatingPointDot(dot):
            newVgsOperatingPoint = ax1.coords_to_point(Vgs(simTime.get_value()), GateSourceToSatCurrent(Vgs(simTime.get_value())))
            newVgsOperatingPointDot = Dot(newVgsOperatingPoint, color=BLUE)
            dot.become(newVgsOperatingPointDot)

        # moves point along with function and time
        VgsOperatingPointLine.add_updater(updateVgsOperatingPointLine)
        VgsOperatingPointDot.add_updater(updateVgsOperatingPointDot)

        # upating the corresponding drain to source graph
        def updateDrainSourceGraph(graph): # TODO remove redundancy from the section when this is set up?
            newDrainSourceGraph = ax2.plot(lambda Vds: DrainSourceToCurrent(Vds, simTime.get_value()), color=WHITE)
            graph.become(newDrainSourceGraph)

        # updaters for draing to source axes (to change graph)
        drainSourceGraph.add_updater(updateDrainSourceGraph)

        # add dots
        self.play(
            Write(VgsOperatingPointLine), 
            Write(VgsOperatingPointDot),
            Write(VdsOperationPointDot), 
            Write(VdsOperatingPointLine)
        )
        # run simulation time forward
        self.play(
            ApplyMethod(simTime.increment_value, 2*5*np.pi, rate_func=rate_functions.smooth),
            run_time=5,
        )

        self.wait(4)

# NOTE RELEVEANT SCENES BELOW (will be cleaned up later)
class BuildMOSFETSymbol(Scene):

    def construct(self):
        # TODO eventually make objects which changable parameters?
        gateWire = Line(LEFT, ORIGIN)
        gateLeftBar = Rectangle(width=0.1, height=1.5, fill_opacity=1).move_to(ORIGIN)
        gateRightBar = Rectangle(width=0.1, height=1.5, fill_opacity=1).move_to(RIGHT*0.5)
        sourceWireRight = Line(RIGHT*0.5+DOWN*1.5/4, RIGHT*1+DOWN*1.5/4) # TODO spacing is a bit ugly I think
        sourceWireDown = Line(RIGHT*1+DOWN*1.5/4, RIGHT*1 + DOWN*1)
        drainWireRight = Line(RIGHT*0.5+UP*1.5/4, RIGHT*1+UP*1.5/4)
        drainWireUp = Line(RIGHT*1+UP*1.5/4, RIGHT*1 + UP*1)
        # technically arrow comes from a line but it has no length and is under the sourceWireRight wire TODO do this a nicer way?
        # TODO make arrow work
        sourceArrow = Arrow() # this is NMOS so arrow goes out toward source

        # add labels to the device
        gateLabel = Text("G", font="Consolas", font_size=30).move_to(LEFT*1.4)
        drainLabel = Text("D", font="Consolas", font_size=30).move_to(RIGHT*1.4 + UP*1) # TODO make these positions dependent on the wire locations rather than hard coded
        sourceLabel = Text("S", font="Consolas", font_size=30).move_to(RIGHT*1.4 + DOWN*1)
        # TODO Make it so writing this group writes source, then gate, then drain
        NMOSLabels = VGroup(gateLabel, drainLabel, sourceLabel)
        
        NMOSCircuitry = VGroup(gateWire, gateLeftBar, gateRightBar, sourceWireRight, sourceWireDown, drainWireRight, drainWireUp)

        NMOSComponent = VGroup(NMOSCircuitry, NMOSLabels)
        NMOSComponent.scale(0.5).move_to(ORIGIN) 

        # Draw surrounding circuitry info
        batteryWirePositive = Line(gateWire.get_start()+DOWN, gateWire.get_start()) # TODO When making class add functions like to get points on MOSFETS

        # draw battery VGroup
        DCBatteryTop = Rectangle(width=1, height=0.07, fill_opacity=1).move_to(UP*0.2)
        DCBatteryBottom = Rectangle(width=0.8, height=0.07, fill_opacity=1)
        DCBatteryCircuitry = VGroup(DCBatteryTop, DCBatteryBottom)

        DCBatteryCircuitry.scale(0.5).move_to(batteryWirePositive.get_start()+DOWN*0.1) # TODO this offset is kind of dumb

        # add labels
        DCBatteryVoltageLabel = Text("Vgs", font="Consolas", font_size=15).move_to(DCBatteryCircuitry.get_left()+LEFT*0.5) # TODO this extra offset is stupid
        DCBatteryPlus = Text("+", font="Consolas", font_size=15).move_to(DCBatteryVoltageLabel.get_top() + UP*0.3)
        DCBatteryMinus = Text("-", font="Consolas", font_size=15).move_to(DCBatteryVoltageLabel.get_bottom() + DOWN*0.3)
        DCBatteryLabels = VGroup(DCBatteryVoltageLabel, DCBatteryPlus, DCBatteryMinus)

        DCBattery = VGroup(DCBatteryCircuitry, DCBatteryLabels)
        
        # Draw wire to ground
        batteryToGround = Line(DCBatteryBottom.get_bottom(), DCBatteryBottom.get_bottom()+DOWN*1)

        # draw ground symbol
        gateGroundTopRect = Rectangle(width=1, height=0.07, fill_opacity=1)
        gateGroundMiddleRect = Rectangle(width=0.7, height=0.07, fill_opacity=1).move_to(DOWN*0.2)
        gateGroundBottomRect = Rectangle(width=0.4, height=0.07, fill_opacity=1).move_to(DOWN*0.4)
        gateGroundSymbol = VGroup(gateGroundTopRect, gateGroundMiddleRect, gateGroundBottomRect)
        gateGroundSymbol.scale(0.5).move_to(batteryToGround.get_bottom()+DOWN*0.1) # TODO this offset is kind of unneeded
    

        # draw power from drain to source
        powerToSourceWire = Line(drainWireUp.get_end(), drainWireUp.get_end() + UP*1)
        
        sourcePower = Rectangle(width=0.5, height=0.035, fill_opacity=1).move_to(powerToSourceWire.get_end())
        sourcePowerLabel = Text("Vs", font="Consolas", font_size=15).move_to(sourcePower.get_top()+UP*0.2) # TODO offset kind of hard coded

        sourcePowerGroup = VGroup(sourcePower, sourcePowerLabel)

        # source to ground wire 
        sourceToGroundWire = Line(sourceWireDown.get_end(), sourceWireDown.get_end()+DOWN*1.65)
        # get source ground TODO make a ground mobject or something so this isn't duplicated
        sourceGroundTopRect = Rectangle(width=1, height=0.07, fill_opacity=1)
        sourceGroundMiddleRect = Rectangle(width=0.7, height=0.07, fill_opacity=1).move_to(DOWN*0.2)
        sourceGroundBottomRect = Rectangle(width=0.4, height=0.07, fill_opacity=1).move_to(DOWN*0.4)
        sourceGroundSymbol = VGroup(sourceGroundTopRect, sourceGroundMiddleRect, sourceGroundBottomRect)
        sourceGroundSymbol.scale(0.5).move_to(sourceToGroundWire.get_end()+DOWN*0.1) # TODO this offset is kind of unneeded

        # wire group to draw
        wires = VGroup(batteryToGround, batteryWirePositive, powerToSourceWire, sourceToGroundWire)

        # group circuit and center
        circuitGroup = VGroup(NMOSComponent, DCBattery, gateGroundSymbol, sourceGroundSymbol, sourcePowerGroup, wires)
        circuitGroup.move_to(ORIGIN)

        # write out circuit
        self.play(Write(NMOSCircuitry))
        self.play(Write(NMOSLabels))
        self.play(Write(DCBatteryCircuitry), Write(DCBatteryLabels))
        self.play(Write(batteryToGround))
        self.play(Write(gateGroundSymbol))
        self.play(Write(sourceGroundSymbol))
        self.play(Write(sourcePower), Write(sourcePowerLabel))
        self.play(Write(wires))

        self.wait(5)

class BuildMOSFETSymbolCircuitKZ(Scene):
    
    def construct(self):
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, american]{circuitikz}")

        """
            \draw (0,0) node[nmos, anchor=G](nmos){};
            \draw (0,0)
            to[V,v=$V_d$] (0,-1.5);
            \draw (0,-1.5)
            to[short] (0,-3)

        """
        """
            \draw (0,0) node[nmos, anchor=G](nmos){};
            \draw (0,0)
            to[V,v=$V_d$] (0,-1.5);
            \draw (0,1.5)
            to[short] (2,1.5)
            to[C=$C$] (2,0)
            to[short] (0,0);
            \draw (2,1.5)
            to[short] (4,-1.5)
            to[R=$R$] (4,0)
            to[short] (2,0);
        """
        """
            \draw (0,0) node[nmos, anchor=G](nmos){};
            \draw (0,0)
            to[battery, invert, l_=$V_d$] (0,-1.5) -- (0, -2) node[ground]{};

            \draw (nmos.gate) to[short, -o] ++(-1, 0);

            \draw 
                (nmos.drain) to[R=$10k\Omega$] ++(0, 1.5);

            \draw
                (nmos.drain) to[short, -o, l_=$V_{out}$] ++(1, 0);

            \draw 
                (nmos.source) -- ++(0, -0.5) node[ground]{};
            
            \draw (2,0) node[above] {$V_{aa}$} to [V, v=$\ $] (2,-2);
        """,
        circuit_allg = MathTex(
            # docs https://texdoc.org/serve/circuitikzmanual.pdf/0
            r"""
            \draw (0,0) node[nmos, anchor=G](nmos){};
            \draw (0,0)
            to[battery, invert, l_=$V_d$] (0,-1.5) -- (0, -2) node[ground]{};

            \draw (nmos.gate) to[short, -o] ++(-1, 0) node[label={left:$v_{in}$}]{};

            \draw 
                (nmos.drain) to[R=$10k\Omega$] ++(0, 1.5) to[short, -o] ++(0, 0.5) node[label={above:$V_{aa}$}]{};

            \draw
                (nmos.drain) to[short, -o] ++(1, 0) node[label={right:$v_{out}$}]{};

            \draw 
                (nmos.source) -- ++(0, -0.5) node[ground]{};
            
            """,
            stroke_width=2
            , fill_opacity=0
            , stroke_opacity=1
            , tex_environment="circuitikz"
            , tex_template=template
            
            )
        circuit_allg.scale(0.5).move_to(ORIGIN)
        self.play(Write(circuit_allg))
        self.wait(3)
        
class MOSFETGraphsSmallSignalInputOutput(Scene):

    def construct(self):
        # set up time 
        simTime = ValueTracker(0)

        # set parameters
        kPrimeWL = 1# TODO make a realistic value
        Vth = 1
        
        # set parameters that are functions
        Vds = lambda t: 4 # constant for the moment # TODO this is done with the operating voltage right now
        Vgs = lambda t: 2 + 0.05*np.sin(t) # TODO this does not have dependence on Vds as it actually does yet = 3
        
        # derived params
        Vod = lambda t: Vgs(t) - Vth
        
        def DrainSourceToCurrent(Vds, t):
            if (Vod(t)<0): # if off return zero
                return 0
            if (Vds<Vod(t)): # less than overdrive, use triode equation
                return kPrimeWL*(Vod(t)*Vds-0.5*(Vds**2))
            else: # in SAT region
                return 0.5*kPrimeWL*((Vod(t))**2) # no lambda for now
            
        def GateSourceToSatCurrent(Vgs):
            if (Vgs<Vth):
                return 0
            else:
                return 0.5*kPrimeWL*((Vgs-Vth)**2)# no lambda for now

        headroom = 0.1 # how much above the max at sat to show as a multiplier
        ax1 = Axes(
            x_range=[0, 3, 1],
            y_range=[0, GateSourceToSatCurrent(3)*(1+headroom), 1],
            tips=False,
            axis_config={"include_numbers": True, "color": WHITE},
            x_length=4,
            y_length=4,
        )
        
        ax1.move_to(LEFT*3)
      
        # graphing parameters
        # get range of drain to source with params to plot properly
        satValue = 0.5*kPrimeWL*((Vod(0))**2)
        ax2 = Axes(
            x_range=[0, 10], # TODO set numbers
            y_range=[0, satValue*(1+headroom)],
            tips=False,
            axis_config={"include_numbers": True, "color": WHITE},
            x_length=4,
            y_length=4,
        )
        ax2.move_to(RIGHT*3)

        # write axes
        self.play(Write(ax1), Write(ax2))
        
        # TODO add stuff below
        gateSourceGraph = ax1.plot(lambda Vgs: GateSourceToSatCurrent(Vgs), x_range=[0, 3], color=WHITE)
        self.play(Write(gateSourceGraph), run_time=3)

        # write curve for each
        drainSourceGraph = ax2.plot(lambda Vds: DrainSourceToCurrent(Vds, simTime.get_value()), color=WHITE)
        self.play(Write(drainSourceGraph), run_time=3)

        # make divider/brace for this region. For the braces just use function values at time 0,
        # because they will be removed before simTime starts going
        satValue = DrainSourceToCurrent(Vod(0), 0)
        linSatPoint = ax2.coords_to_point(Vod(0), satValue)
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
            Write(offRegionBrace),
            Write(offRegionBraceText),
            Write(onRegionBrace),
            Write(onRegionBraceText)
        )
        
        self.wait(4) 
        # remove braces 
        self.play(
            Unwrite(linSatRegionDividerLine), 
            Unwrite(linearRegionBrace),
            Unwrite(linearRegionBraceText),
            Unwrite(satRegionBrace),
            Unwrite(satRegionBraceText),
            Unwrite(onOffDividerLine), # TODO make group for this stuff? this is too much
            Unwrite(offRegionBrace),
            Unwrite(offRegionBraceText),
            Unwrite(onRegionBrace),
            Unwrite(onRegionBraceText)
        )

        # TODO when doign small signal analysis and moving vertical point and dot around together use a VGroup?
        # add operating region dots to the scene
        # Vds shouldn't really vary, but if it does it is set up to be a function here
        # TODO double use of simTime.get_value in DrainSourceToCurrent is bad
        VdsOperatingPoint = ax2.coords_to_point(Vds(simTime.get_value()), DrainSourceToCurrent(Vds(simTime.get_value()), simTime.get_value())) # TODO organize these param numbers
        VdsOperatingPointLine = ax2.get_vertical_line(VdsOperatingPoint, color=BLUE)
        VdsOperationPointDot = Dot(VdsOperatingPoint, color=BLUE)

        # updaters to move this dot up and down (and left and right if needed)
        def updateVdsOperatingPointLine(line):
            newVdsOperatingPoint = ax2.coords_to_point(Vds(simTime.get_value()), DrainSourceToCurrent(Vds(simTime.get_value()), simTime.get_value())) # TODO organize these param numbers
            newVdsOperatingPointLine = ax2.get_vertical_line(newVdsOperatingPoint, color=BLUE)
            line.become(newVdsOperatingPointLine)

        def updateVdsOperatingPointDot(dot):
            newVdsOperatingPoint = ax2.coords_to_point(Vds(simTime.get_value()), DrainSourceToCurrent(Vds(simTime.get_value()), simTime.get_value())) # TODO organize these param numbers
            newVdsOperationPointDot = Dot(newVdsOperatingPoint, color=BLUE)
            dot.become(newVdsOperationPointDot)

        VdsOperatingPointLine.add_updater(updateVdsOperatingPointLine)
        VdsOperationPointDot.add_updater(updateVdsOperatingPointDot)

        # create dot for Vgs and move it with function given
        # Vgs operating point voltage is defined at the top
        VgsOperatingPoint = ax1.coords_to_point(Vgs(simTime.get_value()), GateSourceToSatCurrent(Vgs(simTime.get_value()))) # TODO organize these param numbers
        VgsOperatingPointLine = ax1.get_vertical_line(VgsOperatingPoint, color=BLUE)
        VgsOperatingPointDot = Dot(VgsOperatingPoint, color=BLUE)

        def updateVgsOperatingPointLine(line):
            newVgsOperatingPoint = ax1.coords_to_point(Vgs(simTime.get_value()), GateSourceToSatCurrent(Vgs(simTime.get_value())))
            newVgsOperatingPointLine = ax1.get_vertical_line(newVgsOperatingPoint, color=BLUE)
            line.become(newVgsOperatingPointLine)

        def updateVgsOperatingPointDot(dot):
            newVgsOperatingPoint = ax1.coords_to_point(Vgs(simTime.get_value()), GateSourceToSatCurrent(Vgs(simTime.get_value())))
            newVgsOperatingPointDot = Dot(newVgsOperatingPoint, color=BLUE)
            dot.become(newVgsOperatingPointDot)

        # moves point along with function and time
        VgsOperatingPointLine.add_updater(updateVgsOperatingPointLine)
        VgsOperatingPointDot.add_updater(updateVgsOperatingPointDot)

        # upating the corresponding drain to source graph
        def updateDrainSourceGraph(graph): # TODO remove redundancy from the section when this is set up?
            newDrainSourceGraph = ax2.plot(lambda Vds: DrainSourceToCurrent(Vds, simTime.get_value()), color=WHITE)
            graph.become(newDrainSourceGraph)

        # upating the corresponding gate to source graph (for when axes are moveds)
        def updateGateSourceGraph(graph): # TODO remove redundancy from the section when this is set up?
            newGateSourceGraph = ax1.plot(GateSourceToSatCurrent, color=WHITE)
            graph.become(newGateSourceGraph)

        # updaters for draing to source axes (to change graph)
        drainSourceGraph.add_updater(updateDrainSourceGraph)
        gateSourceGraph.add_updater(updateGateSourceGraph)

        # add dots
        self.play(
            Write(VgsOperatingPointLine), 
            Write(VgsOperatingPointDot),
            Write(VdsOperationPointDot), 
            Write(VdsOperatingPointLine)
        )

        # run simulation time forward
        self.play(
            ApplyMethod(simTime.increment_value, 2*5*np.pi, rate_func=rate_functions.smooth),
            run_time=5,
        )
        simTime.set_value(0) # reset value so can be played with again later without messing up updater functions

        self.wait(4)

        # move and rescale axes
        # TODO give more descriptive name to ax1
        newAx1 = Axes(
            x_range=[0, 2, 1], # shrink x range and corresponding y range
            y_range=[0, GateSourceToSatCurrent(2)*(1+headroom)],
            tips=False,
            axis_config={"include_numbers": True, "color": WHITE},
            x_length=3,
            y_length=3,
        )
        newAx1.move_to(LEFT*3.5+UP*1.1)

        newAx2 = Axes(
            x_range=[0, 10], # TODO set numbers
            y_range=[0, satValue*(1+headroom)],
            tips=False,
            axis_config={"include_numbers": True, "color": WHITE},
            x_length=3,
            y_length=3,
        )
        newAx2.move_to(RIGHT*3+UP*1.1)
        self.play(ax1.animate.become(newAx1), ax2.animate.become(newAx2))

        # TODO make setting up the responsive graphs a function that is done at the top so that they extra stuff can be compartimentalizse better
        # TODO potential reordering here? NOTE it actually worked changing it before playing because the update functions only work with the graphs
        # move plots 
        # TODO tinker with plot sizes so they can move up and out of the way for teh input and output signal to have enough space
        # TODO this another wiggle is unneeded

        # add the little small signal graphs at the bottom that respond to wiggle as well

        # adding small signal graph for gate to source
        inputSignalAxes = Axes(
            x_range=[0, 10], # TODO set numbers
            y_range=[1.7, 2.3, 0.1], # TODO make it set dynamically
            tips=False,
            axis_config={"include_numbers": True, "color": YELLOW},
            x_length=5,
            y_length=3,
        )
        inputSignalAxes.move_to(LEFT*4+DOWN*2)
        inputSignalVgsGraph = inputSignalAxes.plot(Vgs, color=BLUE)
        self.play(Write(inputSignalAxes), Write(inputSignalVgsGraph))
        
        inputSignalPoint = inputSignalAxes.coords_to_point(0, Vgs(0))
        inputSignalDot = Dot(inputSignalPoint, color=RED) # TODO make a VGroup for these so that is functions better?
        inputSignalVerticalLine = inputSignalAxes.get_vertical_line(inputSignalPoint, color=RED)

        # TODO make these updater functions under a larger function since they are all so similar for the dots and the vertical lines
        def updateInputSignalDot(dot):
            newInputSignalPoint = inputSignalAxes.coords_to_point(simTime.get_value(), Vgs(simTime.get_value()))
            newInputSignalDot = Dot(newInputSignalPoint, color=RED)
            dot.become(newInputSignalDot)
        
        def updateInputSignalLine(line):
            newInputSignalPoint = inputSignalAxes.coords_to_point(simTime.get_value(), Vgs(simTime.get_value()))
            newInputSignalLine = inputSignalAxes.get_vertical_line(newInputSignalPoint, color=RED)
            line.become(newInputSignalLine)
        
        # TODO get below working
        inputSignalDot.add_updater(updateInputSignalDot)
        inputSignalVerticalLine.add_updater(updateInputSignalLine)

        self.play(Write(inputSignalDot), Write(inputSignalVerticalLine))

        # adding output graph 
        outputSignalAxes = Axes(
            x_range=[0, 10], # TODO set numbers
            y_range=[0.3, 0.7, 0.1], # TODO make it set dynamically
            tips=False,
            axis_config={"include_numbers": True, "color": YELLOW},
            x_length=5,
            y_length=3,
        )
        outputSignalAxes.move_to(RIGHT*2.5+DOWN*2)
        outputSignalVdsGraph = outputSignalAxes.plot(lambda time: DrainSourceToCurrent(Vds(time), time), color=BLUE)
        self.play(Write(outputSignalAxes), Write(outputSignalVdsGraph))

        outputSignalPoint = outputSignalAxes.coords_to_point(0, DrainSourceToCurrent(Vds(0), 0))
        outputSignalDot = Dot(outputSignalPoint, color=RED)
        outputSignalLine = outputSignalAxes.get_vertical_line(outputSignalPoint, color=RED)

        # TODO make updaters not so redundant
        def updateOutputSignalDot(dot):
            newOutputSignalPoint = outputSignalAxes.coords_to_point(simTime.get_value(), DrainSourceToCurrent(Vds(simTime.get_value()), simTime.get_value()))
            newOutputSignalDot = Dot(newOutputSignalPoint, color=RED)
            dot.become(newOutputSignalDot)

        def updateOutputSignalLine(line):
            newOutputSignalPoint = outputSignalAxes.coords_to_point(simTime.get_value(), DrainSourceToCurrent(Vds(simTime.get_value()), simTime.get_value()))
            newOutputSignalLine = outputSignalAxes.get_vertical_line(newOutputSignalPoint, color=RED)
            line.become(newOutputSignalLine)
        
        outputSignalDot.add_updater(updateOutputSignalDot)
        outputSignalLine.add_updater(updateOutputSignalLine)
        
        self.play(Write(outputSignalDot), Write(outputSignalLine))
        self.play(
            ApplyMethod(simTime.increment_value, 8, rate_func=rate_functions.linear),
            run_time=5,
        )
        simTime.set_value(0) # reset for playing again later

        # add updaters to the graphs so they go forward as inputs 

        # TODO make these updaters less redundant?
        # TODO this does not work right now
        def updateInputSignalVgsGraph(graph):
            newInputSignalVgsGraph = inputSignalAxes.plot(lambda t: Vgs(t), x_range=[0, simTime.get_value()], color=BLUE) 
            graph.become(newInputSignalVgsGraph)

        inputSignalVgsGraph.add_updater(updateInputSignalVgsGraph)

# connects circuit scene and graphing scene together
class BuildMOSFETThenSmallSignal(Scene):
    
    def construct(self):
        BuildMOSFETSymbol.construct(self)
        BuildMOSFETSymbol.clear(self) #  clear for next scene

        MOSFETGraphsSmallSignalInputOutput.construct(self)
        MOSFETGraphsSmallSignalInputOutput.clear(self)