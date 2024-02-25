
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
        VdsOperatingVoltage = 4
        VdsOperatingPoint = ax2.coords_to_point(VdsOperatingVoltage, DrainSourceToCurrent(VdsOperatingVoltage)) # TODO organize these param numbers
        VdsOperatingPointLine = ax2.get_vertical_line(VdsOperatingPoint, color=BLUE)
        self.play(Write(Dot(VdsOperatingPoint, color=BLUE)), Write(VdsOperatingPointLine))

        VgsOperatingVoltage = 1.5 # TODO this does not have dependence on Vds as it actually does yet
        VgsOperatingPoint = ax1.coords_to_point(VgsOperatingVoltage, GateSourceToSatCurrent(VgsOperatingVoltage)) # TODO organize these param numbers
        VgsOperatingPointLine = ax1.get_vertical_line(VgsOperatingPoint, color=BLUE)

        self.play(Write(VgsOperatingPointLine))
        self.play(Write(Dot(VgsOperatingPoint, color=BLUE)))


        self.wait(5)
