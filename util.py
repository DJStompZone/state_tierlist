from bs4 import BeautifulSoup
import os

STATE_IDS = ['AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
STATE_HTML = [f'state_shapes/{state}.html' for state in STATE_IDS]

def get_svg_paths(svg_file):
    """
    Extracts and returns all the path elements from an SVG file except the last one.

    Args:
        svg_file (str): The file path to the SVG file.

    Returns:
        list: A list of BeautifulSoup Tag objects representing the path elements in the SVG file.
    """
    with open(svg_file, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        paths = soup.findChildren('path')[:-1]
        return paths

def get_all_states():
    """
    Retrieves all states from an SVG file and returns them as a dictionary.

    This function reads an SVG file located in the 'templates' directory, extracts
    the paths for each state, and creates a dictionary where the keys are the state
    IDs and the values are StateSVG objects initialized with the attributes of each state.

    Returns:
        dict: A dictionary where the keys are state IDs and the values are StateSVG objects.
    """
    ALL_STATES_PATHS = get_svg_paths(
        os.path.join(os.path.dirname(__file__), 'templates', 'states.html')
    )
    ALL_STATES = {ea.attrs['id']: StateSVG(**ea.attrs) for ea in ALL_STATES_PATHS}
    return ALL_STATES

def get_state_paths():
    """
    Generates a dictionary of state paths.

    This function constructs a dictionary where each key is a state identifier and each value is a list of StateSVG objects. 
    It reads SVG paths from HTML files located in the 'templates/state_shapes' directory, parses them, and converts them into 
    StateSVG objects.

    Returns:
        dict: A dictionary with state identifiers as keys and lists of StateSVG objects as values.
    """
    STATE_PATHS = {state: get_svg_paths(os.path.join(os.path.dirname(__file__), 'templates', f'state_shapes/{state}.html')) for state in STATE_IDS}
    return STATE_PATHS

class StateSVG:
    """
    A class to represent an SVG path element for a state.

    Attributes:
    -----------
    id : str
        The ID of the SVG path element.
    d : str
        The 'd' attribute of the SVG path element, which contains the path data.
    name : str
        The name of the state, stored in the 'data-name' attribute.

    Methods:
    --------
    __str__():
        Returns a string representation of the SVG path element.
    __repr__():
        Returns a string representation of the SVG path element.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.d = kwargs.get('d')
        self.name = kwargs.get('data-name', '')
    def __str__(self):
        return f'<path id="{self.id}" data-name="{self.name}" data-id="{self.id}" d="{self.d}">'
    def __repr__(self):
        return self.__str__()
    
def save_state_html(states):
    for k, ea in states.items():
        with open(f'templates/state_shapes/{k}.html', 'w') as fp:
            state_html = str(ea).replace(' class="', '\n        class="').replace(' d="', '\n        d="').replace(' id="', '\n        id="').replace(' data-id="', '\n        data-id="').replace(' data-name="', '\n        draggable="true"\n        data-name="')[:-1]+"\n/>"
            fp.write(state_html)