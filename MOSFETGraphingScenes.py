from manim import *

class BuildMOSFETCircuitSimple(Scene):
    
    def construct(self):
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, american]{circuitikz}")
        
        simpleMOSFET = MathTex(
            # docs https://texdoc.org/serve/circuitikzmanual.pdf/0
            r"""\draw (0,0) node[nmos, anchor=G](nmos){};

            \draw (nmos.gate) to[short, -o] ++(-1, 0) node[label={left:$v_{in}$}]{};

            \draw
                (nmos.drain) to[short, -o, i<=$I_{out}$] ++(1, 0) node[label={right:$i_{out}$}]{};

            \draw 
                (nmos.source) -- ++(0, -0.25) node[ground]{};     

            """,
            stroke_width=2
            , fill_opacity=0
            , stroke_opacity=1
            , tex_environment="circuitikz"
            , tex_template=template     
            )
        simpleMOSFET.scale(0.5).move_to(ORIGIN)
        self.play(Write(simpleMOSFET))
        self.wait(3)

        simpleMOSFETWithResistor = MathTex(
            # docs https://texdoc.org/serve/circuitikzmanual.pdf/0
            r"""\draw (0,0) node[nmos, anchor=G](nmos){};

            \draw (nmos.gate) to[short] ++(-2, 0) node[label={left:$v_{in}$}]{};

            \draw 
                (nmos.drain) to[R=$R_{1}$] ++(0, 1.5) to[short, -o] ++(0, 0.5) node[label={above:$V_{aa}$}]{};

            \draw
                (nmos.drain) to[short] ++(2, 0) node[label={right:$v_{out}$}]{};

            \draw 
                (nmos.source) to[short, i>=$I_{aa}$] ++(0, -0.25) node[ground]{};     
            """,
            stroke_width=2
            , fill_opacity=0
            , stroke_opacity=1
            , tex_environment="circuitikz"
            , tex_template=template
            
            )
        simpleMOSFETWithResistor.scale(0.5).move_to(ORIGIN+DOWN)

        # draw input signal
        Vgs = lambda t: 2 + 0.05*np.sin(t)
        inputAxes = Axes(
            x_range=[0, 8, 1],
            y_range=[1.8, 2.2, 0.1],
            tips=False,
            axis_config={"include_numbers": True, "color": YELLOW},
            x_length=8,
            y_length=2,
        )
        inputAxes.move_to(LEFT*3.5+UP*0.25).scale(0.4)
        inputSignal = inputAxes.plot(Vgs, color=BLUE)
        inputGraph = VGroup(inputAxes, inputSignal)
        self.play(Write(inputAxes), Write(inputSignal))
        self.wait(3)

        # assuming sat, can write equation
        satRegionText = Tex("Assuming that the MOSFET is in saturation, we have an equation for $I_{out}$")
        satRegionText.move_to(UP*3).scale(0.7)
        self.play(Write(satRegionText))
        satEquation = MathTex("i_{DS}", r"=\frac{1}{2}k'\frac{W}{L}\cdot(", "V_{GS}", "-V_{th})^{2}", color=RED_B)
        satEquation.move_to(UP*2)
        self.play(Write(satEquation))
        equationRectangleVgs = SurroundingRectangle(satEquation[2], buff=0.1)
        self.play(Write(equationRectangleVgs))
        self.wait(0.5)

        # substitute V_in
        satEquationVinCopy = MathTex("i_{DS}", r"=\frac{1}{2}k'\frac{W}{L}\cdot(", "v_{in}", "-V_{th})^{2}", color=RED_B) # TODO make this not just a copied duplicate but actually done properly
        satEquationVinCopy[2].set_color(color=BLUE)
        satEquationVinCopy.move_to(UP*2) # NOTE hardcoded movement to match the earlier equation
        self.play(ReplacementTransform(satEquation, satEquationVinCopy)) # NOTE settings are the same and hard coded

        # slide reactangle over to replace I_ds
        equationRectangleIds = SurroundingRectangle(satEquation[0], buff=0.1)
        self.play(ReplacementTransform(equationRectangleVgs,equationRectangleIds))
        self.wait(0.5)
        # TODO again make the copy nicer rather than hard coded
        satEquationIoutCopy = MathTex("i_{out}", r"=\frac{1}{2}k'\frac{W}{L}\cdot(", "v_{in}", "-V_{th})^{2}", color=RED_B) # TODO make this not just a copied duplicate but actually done properly
        satEquationIoutCopy[0].set_color(color=BLUE)
        satEquationIoutCopy[2].set_color(color=BLUE)
        satEquationIoutCopy.move_to(UP*2) # NOTE hardcoded movement to match the earlier equation
        self.play(ReplacementTransform(satEquationVinCopy, satEquationIoutCopy))
        self.play(Unwrite(equationRectangleIds))
        self.wait(3)

        # new text for Iout
        IoutText = Tex("Adding a resistor, this $I_{out}$ can create an output voltage")
        IoutText.move_to(UP*3).scale(0.7)
        self.play(FadeOut(satRegionText))
        self.play(Write(IoutText))
        self.wait(2)

        # change to new circuit
        satEquationIdsCopy = MathTex("i_{aa}", r"=\frac{1}{2}k'\frac{W}{L}\cdot(", "v_{in}", "-V_{th})^{2}", color=RED_B) # TODO make this not just a copied duplicate but actually done properly
        satEquationIdsCopy[0].set_color(color=BLUE)
        satEquationIdsCopy[2].set_color(color=BLUE)
        satEquationIdsCopy.move_to(UP*2) # NOTE hardcoded movement to match the earlier equation
        self.play(ReplacementTransform(simpleMOSFET, simpleMOSFETWithResistor), 
                  inputGraph.animate.move_to(LEFT*4.3 + DOWN*1.5),
                  ReplacementTransform(satEquationIoutCopy, satEquationIdsCopy))
        self.wait(2)


        # doing a bunch of algebra for terms of vout

        # replace Ids with ohms law
        satEquationIdsReplacedCopy = MathTex(r"\frac{V_{aa}-v_{out}}{R_{1}}", r"=\frac{1}{2}k'\frac{W}{L}\cdot(", "v_{in}", "-V_{th})^{2}", color=RED_B) # TODO make this not just a copied duplicate but actually done properly
        satEquationIdsReplacedCopy.move_to(UP*2) # NOTE hardcoded movement to match the earlier equation
        self.play(ReplacementTransform(satEquationIdsCopy, satEquationIdsReplacedCopy), run_time=1)
        
        satEquationIdsMultipliedByR1 = MathTex(r"V_{aa}-v_{out}", r"=R_{1}\cdot\frac{1}{2}k'\frac{W}{L}\cdot(", "v_{in}", "-V_{th})^{2}", color=RED_B)
        satEquationIdsMultipliedByR1.move_to(UP*2) # NOTE hardcoded movement to match the earlier equation
        self.play(ReplacementTransform(satEquationIdsReplacedCopy, satEquationIdsMultipliedByR1), run_time=1) # TODO fix rewriting bug

        satEquationDone = MathTex(r"v_{out}=", r"V_{aa}", r"-", r"R_{1}", r"\cdot", r"\frac{1}{2}k'\frac{W}{L}", r"\cdot", "(v_{in}-", "V_{th}", ")^{2}", color=RED_B)
        satEquationDone.move_to(UP*2)
        self.play(ReplacementTransform(satEquationIdsMultipliedByR1, satEquationDone))
        self.wait(2)
        
        # new text
        constantInfoText = Tex("Everything in blue is just a constant.")
        constantInfoText.move_to(UP*3).scale(0.7)
        self.play(FadeOut(IoutText))
        self.play(Write(constantInfoText),
                  satEquationDone[1].animate.set_color(BLUE_B), 
                  satEquationDone[3].animate.set_color(BLUE_B),
                  satEquationDone[5].animate.set_color(BLUE_B),
                  satEquationDone[8].animate.set_color(BLUE_B))
        self.wait(5)

class MOSFETGraphsSmallSignalInputOutput(Scene):

    def construct(self):
        # set up time 
        simTime = ValueTracker(0) # NOTE: Can probably use manim's built in move along path for some of the uses of this

        # set parameters
        kPrimeWL = 2 # TODO make a realistic value
        Vth = 0.6
        
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
            y_range=[0, GateSourceToSatCurrent(3)*(1+headroom)],
            tips=False,
            axis_config={"include_numbers": True, "color": WHITE},
            x_length=4,
            y_length=4,
        )
        
        ax1.move_to(LEFT*3) 
        ax1XLabel = ax1.get_x_axis_label('V_{gs}').shift(DOWN*0.2).set_color(RED_B) # indicate as input
        ax1YLabel = ax1.get_y_axis_label('I_{sat}').shift(LEFT)
      
        # graphing parameters
        # get range of drain to source with params to plot properly
        satValue = 0.5*kPrimeWL*((Vod(0))**2)
        ax2 = Axes(
            x_range=[0, 10, 2], # TODO set numbers
            y_range=[0, satValue*(1+headroom), 0.5], # TODO make ticks a variable
            tips=False,
            axis_config={"include_numbers": True, "color": WHITE},
            x_length=4,
            y_length=4,
        )
        ax2.move_to(RIGHT*3)
        ax2XLabel = ax2.get_x_axis_label('V_{ds}').shift(DOWN*0.2)
        ax2YLabel = ax2.get_y_axis_label('I_{ds}').shift(LEFT).set_color(RED_B) # indicate as output
      
        # write axes
        self.play(Write(ax1), Write(ax1XLabel), Write(ax1YLabel),
                  Write(ax2), Write(ax2XLabel), Write(ax2YLabel))
        
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
        VdsOperatingPointLine = ax2.get_vertical_line(VdsOperatingPoint, color=GREEN)
        VdsOperationPointDot = Dot(VdsOperatingPoint, color=GREEN)

        # updaters to move this dot up and down (and left and right if needed)
        def updateVdsOperatingPointLine(line):
            newVdsOperatingPoint = ax2.coords_to_point(Vds(simTime.get_value()), DrainSourceToCurrent(Vds(simTime.get_value()), simTime.get_value())) # TODO organize these param numbers
            newVdsOperatingPointLine = ax2.get_vertical_line(newVdsOperatingPoint, color=GREEN)
            line.become(newVdsOperatingPointLine)

        def updateVdsOperatingPointDot(dot):
            newVdsOperatingPoint = ax2.coords_to_point(Vds(simTime.get_value()), DrainSourceToCurrent(Vds(simTime.get_value()), simTime.get_value())) # TODO organize these param numbers
            newVdsOperationPointDot = Dot(newVdsOperatingPoint, color=GREEN)
            dot.become(newVdsOperationPointDot)

        VdsOperatingPointLine.add_updater(updateVdsOperatingPointLine)
        VdsOperationPointDot.add_updater(updateVdsOperatingPointDot)

        # create dot for Vgs and move it with function given
        # Vgs operating point voltage is defined at the top
        VgsOperatingPoint = ax1.coords_to_point(Vgs(simTime.get_value()), GateSourceToSatCurrent(Vgs(simTime.get_value()))) # TODO organize these param numbers
        VgsOperatingPointLine = ax1.get_vertical_line(VgsOperatingPoint, color=RED)
        VgsOperatingPointDot = Dot(VgsOperatingPoint, color=BLUE)

        def updateVgsOperatingPointLine(line):
            newVgsOperatingPoint = ax1.coords_to_point(Vgs(simTime.get_value()), GateSourceToSatCurrent(Vgs(simTime.get_value())))
            newVgsOperatingPointLine = ax1.get_vertical_line(newVgsOperatingPoint, color=RED)
            line.become(newVgsOperatingPointLine)

        def updateVgsOperatingPointDot(dot):
            newVgsOperatingPoint = ax1.coords_to_point(Vgs(simTime.get_value()), GateSourceToSatCurrent(Vgs(simTime.get_value())))
            newVgsOperatingPointDot = Dot(newVgsOperatingPoint, color=RED)
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

        # write text
        # Split the text into substrings
        smallChangeDescription = Tex(r"A small change to the input (", r"$V_{gs}$", r") will produce corresponding change in current (" ,r"$I_{ds}$", r").", color=WHITE).move_to(UP*3.5).scale(0.7)

        smallChangeDescription[1].set_color(RED_B)
        smallChangeDescription[3].set_color(RED_B)

        self.play(Write(smallChangeDescription))
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
            x_range=[0, 3, 1], # shrink x range and corresponding y range
            y_range=[0, GateSourceToSatCurrent(3)*(1+headroom)], # TODO make theses proper labels
            tips=False,
            axis_config={"include_numbers": True, "color": WHITE},
            x_length=3,
            y_length=3,
        )
        newAx1.move_to(LEFT*3.5+UP*1.1)
        newAx1XLabel = newAx1.get_x_axis_label('V_{gs}').scale(0.8).shift(DOWN*0.1).set_color(RED_B)
        newAx1YLabel = newAx1.get_y_axis_label('I_{sat}').shift(LEFT*0.5).scale(0.8).set_color(RED_B)

        newAx2 = Axes(
            x_range=[0, 10, 2], # TODO set numbers
            y_range=[0, satValue*(1+headroom), 0.5],
            tips=False,
            axis_config={"include_numbers": True, "color": WHITE},
            x_length=3,
            y_length=3,
        )

        newAx2.move_to(RIGHT*3+UP*1.1)
        newAx2XLabel = newAx2.get_x_axis_label('V_{ds}').shift(DOWN*0.1).scale(0.8)
        newAx2YLabel = newAx2.get_y_axis_label('I_{ds}').shift(LEFT*0.5).scale(0.8).set_color(RED_B)
        self.play(ax1.animate.become(newAx1), 
                  ax1XLabel.animate.become(newAx1XLabel),
                  ax1YLabel.animate.become(newAx1YLabel), 
                  ax2.animate.become(newAx2),
                  ax2XLabel.animate.become(newAx2XLabel),
                  ax2YLabel.animate.become(newAx2YLabel)
                  )

        # TODO make setting up the responsive graphs a function that is done at the top so that they extra stuff can be compartimentalizse better
        # TODO potential reordering here? NOTE it actually worked changing it before playing because the update functions only work with the graphs
        # move plots 
        # TODO tinker with plot sizes so they can move up and out of the way for teh input and output signal to have enough space

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
            y_range=[1.7, 2.3, 0.1], # TODO make it set dynamically
            tips=False,
            axis_config={"include_numbers": True, "color": YELLOW},
            x_length=5,
            y_length=3,
        )
        outputSignalAxes.move_to(RIGHT*2.5+DOWN*2)
        outputSignalVdsGraph = outputSignalAxes.plot(lambda time: DrainSourceToCurrent(Vds(time), time), color=BLUE) # TODO make work better, but note multiplied to put into mA
        self.play(Write(outputSignalAxes), Write(outputSignalVdsGraph))

        outputSignalPoint = outputSignalAxes.coords_to_point(0, DrainSourceToCurrent(Vds(0), 0))
        outputSignalDot = Dot(outputSignalPoint, color=RED)
        outputSignalLine = outputSignalAxes.get_vertical_line(outputSignalPoint, color=GREEN)

        # TODO make updaters not so redundant
        def updateOutputSignalDot(dot):
            newOutputSignalPoint = outputSignalAxes.coords_to_point(simTime.get_value(), DrainSourceToCurrent(Vds(simTime.get_value()), simTime.get_value()))
            newOutputSignalDot = Dot(newOutputSignalPoint, color=GREEN)
            dot.become(newOutputSignalDot)

        def updateOutputSignalLine(line):
            newOutputSignalPoint = outputSignalAxes.coords_to_point(simTime.get_value(), DrainSourceToCurrent(Vds(simTime.get_value()), simTime.get_value()))
            newOutputSignalLine = outputSignalAxes.get_vertical_line(newOutputSignalPoint, color=GREEN)
            line.become(newOutputSignalLine)
        
        outputSignalDot.add_updater(updateOutputSignalDot)
        outputSignalLine.add_updater(updateOutputSignalLine)
        
        self.play(Write(outputSignalDot), Write(outputSignalLine))
        self.play(
            ApplyMethod(simTime.increment_value, 10, rate_func=rate_functions.linear),
            run_time=5,
        )
        self.wait(1)
        simTime.set_value(0) # reset for playing again later

        # add updaters to the graphs so they go forward as inputs 

        # TODO make these updaters less redundant?
        # TODO this does not work right now
        def updateInputSignalVgsGraph(graph):
            newInputSignalVgsGraph = inputSignalAxes.plot(lambda t: Vgs(t), x_range=[0, simTime.get_value()], color=BLUE) 
            graph.become(newInputSignalVgsGraph)

        inputSignalVgsGraph.add_updater(updateInputSignalVgsGraph)
        
class BuildMOSFETCircuitCommonSourceDCOffsets(Scene):
    
    def construct(self):
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, american]{circuitikz}")
  
        circuit_allg = MathTex(
            # docs https://texdoc.org/serve/circuitikzmanual.pdf/0
            r"""\draw (0,0) node[nmos, anchor=G](nmos){};

            \draw (nmos.gate) to[short] ++(-2, 0) node[label={left:$v_{in}$}]{};

            \draw 
                (nmos.drain) to[R=$10k\Omega$] ++(0, 1.5) to[short, -o] ++(0, 0.5) node[label={above:$V_{aa}$}]{};

            \draw
                (nmos.drain) to[short] ++(2, 0) node[label={right:$v_{out}$}]{};

            \draw 
                (nmos.source) -- ++(0, -0.25) node[ground]{};     
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
    
        circuit_allg_dc = MathTex(
            # docs https://texdoc.org/serve/circuitikzmanual.pdf/0
            r"""\draw (0,0) node[nmos, anchor=G](nmos){};"""
            r"""\draw (0,0) to[battery, invert, l_=$V_d$] (0,-1.5) -- (0, -2) node[ground]{};

            \draw (nmos.gate) to[short] ++(-1, 0) to[C, l_=BIG, -o] ++(-1, 0) node[label={left:$v_{in}$}]{};

            \draw 
                (nmos.drain) to[R=$10k\Omega$] ++(0, 1.5) to[short, -o] ++(0, 0.5) node[label={above:$V_{aa}$}]{};

            \draw
                (nmos.drain) to[short] ++(1, 0) to[C, l^=BIG, -o] ++(1, 0) node[label={right:$v_{out}$}]{};

            \draw 
                (nmos.source) -- ++(0, -0.25) node[ground]{};     
            """,
            stroke_width=2
            , fill_opacity=0
            , stroke_opacity=1
            , tex_environment="circuitikz"
            , tex_template=template
            )
        circuit_allg_dc.scale(0.5).move_to(ORIGIN)
        
        DCOffsetInfoLine1 = Text("In practice, we must have a DC offset at the gate")
        DCOffsetInfoLine2 = Text(" to actually remain in saturation, which before we were assuming was the case.")
        DCOffsetInfo = VGroup(DCOffsetInfoLine1, DCOffsetInfoLine2)
        DCOffsetInfo.arrange(DOWN, buff=0.5)
        DCOffsetInfo.scale(0.4).move_to(UP*3.5)
        DCOffsetHighlightRectangle = Rectangle(height=4, width=2, color=RED_B).scale(0.6).move_to(ORIGIN+0.5*LEFT+DOWN)
        self.play(ReplacementTransform(circuit_allg, circuit_allg_dc), Write(DCOffsetInfo), run_time=1)  
        self.play(FadeIn(DCOffsetHighlightRectangle))   
        self.play(Shake(DCOffsetHighlightRectangle))   
        self.wait(3)   
        
# connects circuit scene and graphing scene together
class BuildMOSFETThenSmallSignal(Scene):
    
    def construct(self):
        BuildMOSFETCircuitSimple.construct(self)
        BuildMOSFETCircuitSimple.clear(self) #  clear for next scene

        MOSFETGraphsSmallSignalInputOutput.construct(self)
        MOSFETGraphsSmallSignalInputOutput.clear(self)

        BuildMOSFETCircuitCommonSourceDCOffsets.construct(self)
        BuildMOSFETCircuitCommonSourceDCOffsets.clear(self) #  clear for next scene