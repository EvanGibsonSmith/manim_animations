from manim import *

class MOSFETGraphs(Scene):
    def construct(self):
        # set parameters
        kPrimeWL = 1
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
        Vth = 0.4
        
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
            ApplyMethod(simTime.increment_value, 10, rate_func=rate_functions.double_smooth),
            run_time=2,
        )

        self.wait(4)
