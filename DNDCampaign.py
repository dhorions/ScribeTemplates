from fpdf import FPDF
import math


class PDF(FPDF):
    def __init__(self, font_family="Helvet", font_size=12):
        super().__init__()
        self.current_title = ''  # Title for the current page
        self.font_family = font_family  # Set the font family
        self.font_size = font_size  # Set the font size

    def header(self):
        # Add a header with a background color and title
        self.set_fill_color(200, 220, 255)  # Light blue background
        self.rect(0, 0, 210, 22, 'F')  # Header rectangle
        self.set_font(self.font_family, "", 10)  # Use configurable font
        self.set_text_color(0)
        self.cell(0, 20, self.current_title, ln=True, align='L')

    def footer(self):
        # Add a footer with a page number
        self.set_y(-15)
        self.set_font(self.font_family, "I", 8)  # Use configurable font for footer
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


# Create PDF instance with configurable font (default: Helvetica)
font = "Helvetica"
pdf = PDF(font_family=font, font_size=12)

# Configuration: Set the number of pages for each section
num_story_pages = 1
num_character_pages = 10  # Number of pages for the Notes section
num_todo_pages = 10  # Number of pages for the To Do section
num_people_pages = 10  # Number of pages for the People section

# Define constants
project_box_height = 15
project_box_width = 150
page_height = 297  # Height of an A4 page in mm
margin_top = 10  # Top margin
margin_bottom = 10  # Bottom margin
margin = 0
icon_size = 10
icon_nav_x = 150  # Position for icons (top-right navigation)
icon_nav_y = 5  # Vertically adjust icons to align in the middle of the header
line_spacing = 10  # Space between the lines for lined paper

# Dummy icons paths
notes_icon = 'images/icons/journal-alt.png'
todo_icon = 'images/icons/to-do.png'
people_icon = 'images/icons/users-alt.png'
home_icon = 'images/icons/home.png'
sections = [
    {"title": "Story", "icon": "images/icons/story.png", "pages": 3, "background": "lined", "hasIndex": "false"},
    {"title": "Mechanics", "icon": "images/icons/mechanics.png", "pages": 3, "background": "lined", "hasIndex": "false"},
    {"title": "Maps", "icon": "images/icons/maps.png", "pages": 5, "background": "hex", "hasIndex": "true"},
    {"title": "Encounters", "icon": "images/icons/encounters.png", "pages": 5, "background": "lined", "hasIndex": "true"},
    {"title": "Friendly NPC's", "icon": "images/icons/npcs.png", "pages": 15, "background": "lined",
     "hasIndex": "true"},
    {"title": "Enemy NPC's", "icon": "images/icons/enemies.png", "pages": 15, "background": "lined", "hasIndex": "true"},
    {"title": "Additional Sections", "icon": "images/icons/additional_topics.png", "pages": 10, "background": "lined",
     "hasIndex": "true"}
]

# Add a cover image on the first page
pdf.add_page()

# Assuming the cover image is named 'cover_image.jpg' and is located in the same directory
cover_image_path = 'images/projectnotes_1.jpg'
pdf.image(cover_image_path, x=0, y=0, w=210, h=297)  # Set the image to cover the full page (A4 size 210x297 mm)


# Function to draw lined paper
def add_lined_page():
    pdf.set_draw_color(200, 200, 200)  # Light gray line
    y = 40
    while y < 290:  # Draw lines from top to bottom of the page (A4 page is 297 mm tall)
        pdf.line(10, y, 200, y)  # Draw a horizontal line from left to right
        y += line_spacing


# Function to draw a lined page with checkboxes (for To Do section)
def add_lined_page_with_checkboxes():
    pdf.set_draw_color(0, 0, 0)  # Black checkboxes
    y = 40
    box_size = 8  # Larger checkbox for easier touch input
    while y < 290:
        # Draw larger checkbox
        pdf.rect(10, y - (box_size), box_size, box_size)
        # Draw horizontal line for To Do items
        pdf.line(20, y, 200, y)
        y += line_spacing


def draw_hexagon(x_center, y_center, size):
    """ Draws a hexagon with a given center (x_center, y_center) and size (distance from center to corner) """
    angle = math.pi / 3  # 60 degrees for each angle in a hexagon
    vertices = []

    # Calculate the vertices of the hexagon
    for i in range(6):
        x = x_center + size * math.cos(i * angle)
        y = y_center + size * math.sin(i * angle)
        vertices.append((x, y))

    # Draw the hexagon by connecting the vertices
    pdf.set_draw_color(200, 200, 200)  # Light gray for hexagon borders
    pdf.set_line_width(0.5)
    for i in range(6):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % 6]
        pdf.line(x1, y1, x2, y2)


def draw_hexagon_background(hex_size):
    """ Fills the entire page with a hexagon background """
    page_width = 210  # A4 page width in mm
    page_height = 297  # A4 page height in mm
    x_offset = 1.5 * hex_size  # Horizontal distance between hexagon centers
    y_offset = math.sqrt(3) * hex_size  # Vertical distance between hexagon centers

    # Fill the entire page with hexagons
    for y in range(0, int(page_height // y_offset) + 2):
        for x in range(0, int(page_width // x_offset) + 2):
            # Offset every second row to create a hexagonal grid
            x_center = x * x_offset
            y_center = y * y_offset + (x % 2) * (y_offset / 2)
            draw_hexagon(x_center, y_center, hex_size)


def add_hexagon_page():
    draw_hexagon_background(15)  # Adjust the size of hexagons if needed


def add_toolbar():
    # Add navigation icons at the top-right corner, centered in the header
    icon_nav_x = 200 - len(sections * icon_size)
    for section in sections:
        pdf.image(section["icon"], x=icon_nav_x, y=icon_nav_y, w=icon_size, h=icon_size, link=section_links[section["title"]])
        icon_nav_x = icon_nav_x + icon_size


# Set the fonts and colors for a professional look
pdf.set_font(pdf.font_family, "B", 16)  # Configurable font
pdf.set_text_color(0)

# Calculate how many projects can fit on a single page
available_height = page_height - margin_top - margin_bottom
projects_per_page = int(available_height // (project_box_height + 5)) - 1  # Correct calculation for projects per page

# Project list with clickable icons for Notes, To Do, and People sections
section_links = dict()  # To store links for the sections

for section in sections:
    section_links[section["title"]] = pdf.add_link()

# Calculate how many projects can fit on a single page
available_height = page_height - margin_top - margin_bottom
projects_per_page = int(available_height // (project_box_height + 5)) - 1  # Correct calculation for projects per page

for section in sections:
    pdf.current_title = section["title"]
    pdf.add_page()
    add_toolbar()
    pdf.set_link(section_links[section["title"]])
    #Add the List page for this section
    item_links = []
    if (section["hasIndex"] == "true"):

        #for i in range(1, projects_per_page + 1):
        i= 0;#index of box on page
        for p in range(section["pages"]):
            i = i + 1
            y_position = margin_top + ((i) * (project_box_height + 5))
            pdf.set_xy(10, y_position)

            # Project Name (Professional look with background fill)
            pdf.set_fill_color(220, 230, 240)  # Light gray-blue fill
            pdf.cell(project_box_width, project_box_height, "", border=1, ln=False, fill=True)

            # Create link points for Notes, To Do, and People
            item_link = pdf.add_link()

            # Add clickable icons for link to page
            pdf.image(section["icon"], x=project_box_width + (1 * 15), y=y_position, w=icon_size, h=icon_size,
                      link=item_link)
            item_links.append(item_link)
            if i >= projects_per_page:
                pdf.add_page()
                add_toolbar()
                i = 0

    for p in range(section["pages"]):
        pdf.add_page()
        add_toolbar()
        if section["hasIndex"] == "true":
            pdf.set_link(item_links[p])

        match section["background"]:
            case "lined":
                add_lined_page()
            case "hex":
                add_hexagon_page()

# Output the PDF to a file
pdf_output_path = "DND Campaign.pdf"
pdf.output(pdf_output_path)

print(f"PDF generated: {pdf_output_path}")
