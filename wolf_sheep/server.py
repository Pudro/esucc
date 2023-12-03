import mesa
import os

from wolf_sheep.agents import SoilPatch, Grass, Bush, Tree
from wolf_sheep.model import WolfSheep

script_dir = os.path.dirname(os.path.realpath(__file__))

def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    # if type(agent) is Sheep:
    #     portrayal["Shape"] = os.path.join(script_dir, "resources/sheep.png")
    #     # https://icons8.com/web-app/433/sheep
    #     portrayal["scale"] = 0.9
    #     portrayal["Layer"] = 1

    # elif type(agent) is Wolf:
    #     portrayal["Shape"] = os.path.join(script_dir, "resources/wolf.png")
    #     # https://icons8.com/web-app/36821/German-Shepherd
    #     portrayal["scale"] = 0.9
    #     portrayal["Layer"] = 2
    #     portrayal["text"] = round(agent.energy, 1)
    #     portrayal["text_color"] = "White"

    if type(agent) is SoilPatch:
        if agent.level == 0:
            portrayal["Color"] = "#D2B48C" #["#00FF00", "#00CC00", "#009900"]
        elif agent.level == 1:
            portrayal["Color"] = "#9C814A"
        elif agent.level == 2:
            portrayal["Color"] = "#67552D"
        else:
            portrayal["Color"] = "#000000"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Grass:
        if agent.fully_grown:
            portrayal["Shape"] = os.path.join(script_dir, "resources/grass_2.png")
        else:
            portrayal["Shape"] = os.path.join(script_dir, "resources/grass.png")
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = agent.countdown, agent.countup
        portrayal["text_color"] = "White"
    
    elif type(agent) is Bush:
        portrayal["Shape"] = os.path.join(script_dir, "resources/bush.png")
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = agent.countup
        portrayal["text_color"] = "White"

    elif type(agent) is Tree:
        portrayal["Shape"] = os.path.join(script_dir, "resources/tree.png")
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text_color"] = "White"

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = mesa.visualization.ChartModule(
    [
        # {"Label": "Wolves", "Color": "#AA0000"},
        # {"Label": "Sheep", "Color": "#666666"},
        {"Label": "Soil", "Color": "#00AA00"},
    ]
)

model_params = {
    # The following line is an example to showcase StaticText.
    "title": mesa.visualization.StaticText("Parameters:"),
    # "grass": mesa.visualization.Checkbox("Grass Enabled", True),
    "soil": mesa.visualization.Checkbox("Grass Enabled", True),

    "grass_regrowth_time": mesa.visualization.Slider("Grass Regrowth Time", 20, 1, 50),
    "initial_sheep": mesa.visualization.Slider(
        "Initial Sheep Population", 100, 10, 300
    ),
    "sheep_reproduce": mesa.visualization.Slider(
        "Sheep Reproduction Rate", 0.04, 0.01, 1.0, 0.01
    ),
    "initial_wolves": mesa.visualization.Slider("Initial Wolf Population", 50, 10, 300),
    "wolf_reproduce": mesa.visualization.Slider(
        "Wolf Reproduction Rate",
        0.05,
        0.01,
        1.0,
        0.01,
        description="The rate at which wolf agents reproduce.",
    ),
    "wolf_gain_from_food": mesa.visualization.Slider(
        "Wolf Gain From Food Rate", 20, 1, 50
    ),
    "sheep_gain_from_food": mesa.visualization.Slider("Sheep Gain From Food", 4, 1, 10),
    "grass_evolution_time": mesa.visualization.Slider("Grass evolution time", 4, 1, 10),
    "bush_evolution_time": mesa.visualization.Slider("Bush evolution time", 4, 1, 10),
    "soil_evolution_time": mesa.visualization.Slider("Soil evolution time", 4, 1, 10),

}

server = mesa.visualization.ModularServer(
    WolfSheep, [canvas_element, chart_element], "Wolf Sheep Predation", model_params
)
server.port = 8521
