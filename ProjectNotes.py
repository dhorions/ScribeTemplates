from fpdf import FPDF

class PDF(FPDF):
    def __init__(self, font_family='Helvetica', font_size=12):
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
pdf = PDF(font_family='Helvetica', font_size=12)

# Configuration: Set the number of pages for each section
num_project_list_pages = 1  # Number of pages for the project list
num_notes_pages = 10  # Number of pages for the Notes section
num_todo_pages = 10  # Number of pages for the To Do section
num_people_pages = 10  # Number of pages for the People section

# Define constants
project_box_height = 15
project_box_width = 150
page_height = 297           # Height of an A4 page in mm
margin_top = 10             # Top margin
margin_bottom = 10          # Bottom margin
margin = 0
icon_size = 10
icon_nav_x = 150  # Position for icons (top-right navigation)
icon_nav_y = 5    # Vertically adjust icons to align in the middle of the header
line_spacing = 10  # Space between the lines for lined paper

# Dummy icons paths
notes_icon = 'images/icons/journal-alt.png'
todo_icon = 'images/icons/to-do.png'
people_icon = 'images/icons/users-alt.png'
home_icon = 'images/icons/home.png'

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

# Set the fonts and colors for a professional look
pdf.set_font(pdf.font_family, "B", 16)  # Configurable font
pdf.set_text_color(0)

# Calculate how many projects can fit on a single page
available_height = page_height - margin_top - margin_bottom
projects_per_page = int(available_height // (project_box_height + 5)) - 1  # Correct calculation for projects per page

# Project list with clickable icons for Notes, To Do, and People sections
project_links = []  # To store links for the project-specific sections
projects_link = pdf.add_link()
pdf.current_title = "Project Notes"
for page_num in range(num_project_list_pages):
    pdf.add_page()
    if page_num == 0:
        pdf.set_link(projects_link)
        #pdf.bookmark("Project List", 0)

    for i in range(1, projects_per_page + 1):
        y_position = margin_top + ((i) * (project_box_height + 5))
        pdf.set_xy(10, y_position)

        # Project Name (Professional look with background fill)
        pdf.set_fill_color(220, 230, 240)  # Light gray-blue fill
        pdf.cell(project_box_width, project_box_height, "", border=1, ln=False, fill=True)

        # Create link points for Notes, To Do, and People
        link_notes = pdf.add_link()
        link_todo = pdf.add_link()
        link_people = pdf.add_link()

        # Add clickable icons for Notes, To Do, and People
        pdf.image(notes_icon, x=project_box_width + (1 * 15), y=y_position, w=icon_size, h=icon_size, link=link_notes)
        pdf.image(todo_icon, x=project_box_width + (2 * 15), y=y_position, w=icon_size, h=icon_size, link=link_todo)
        pdf.image(people_icon, x=project_box_width + (3 * 15), y=y_position, w=icon_size, h=icon_size, link=link_people)

        # Store the links for project sections to be used in the next loop
        project_links.append((link_notes, link_todo, link_people))

# Create pages for Notes, To Do, and People for each project based on the configurable number of pages
for i in range(1, len(project_links) + 1):
    link_notes, link_todo, link_people = project_links[i - 1]

    # Create Notes section
    for notes_page in range(num_notes_pages):
        pdf.current_title = f"Notes - {notes_page + 1} / {num_notes_pages}"  # Set header title dynamically
        pdf.add_page()
        if notes_page == 0:
            pdf.set_link(link_notes)

        # Add navigation icons at the top-right corner, centered in the header
        pdf.image(home_icon, x=icon_nav_x, y=icon_nav_y, w=icon_size, h=icon_size, link=projects_link)
        pdf.image(todo_icon, x=icon_nav_x + 15, y=icon_nav_y, w=icon_size, h=icon_size, link=link_todo)
        pdf.image(people_icon, x=icon_nav_x + 30, y=icon_nav_y, w=icon_size, h=icon_size, link=link_people)
        pdf.image(notes_icon, x=icon_nav_x + 45, y=icon_nav_y, w=icon_size, h=icon_size, link=link_notes)

        # Add lined paper effect
        add_lined_page()

    # Create To Do section
    for todo_page in range(num_todo_pages):
        pdf.current_title = f"To Do - {todo_page + 1} / {num_todo_pages}"  # Set header title dynamically
        pdf.add_page()
        if todo_page == 0:
            pdf.set_link(link_todo)

        # Add navigation icons at the top-right corner, centered in the header
        pdf.image(home_icon, x=icon_nav_x, y=icon_nav_y, w=icon_size, h=icon_size, link=projects_link)
        pdf.image(todo_icon, x=icon_nav_x + 15, y=icon_nav_y, w=icon_size, h=icon_size, link=link_todo)
        pdf.image(people_icon, x=icon_nav_x + 30, y=icon_nav_y, w=icon_size, h=icon_size, link=link_people)
        pdf.image(notes_icon, x=icon_nav_x + 45, y=icon_nav_y, w=icon_size, h=icon_size, link=link_notes)

        # Add lined page with checkboxes for To Do section
        add_lined_page_with_checkboxes()

    # Create People section
    for people_page in range(num_people_pages):
        pdf.current_title = f"People - {people_page + 1} / {num_people_pages}"  # Set header title dynamically
        pdf.add_page()
        if people_page == 0:
            pdf.set_link(link_people)

        # Add navigation icons at the top-right corner, centered in the header
        pdf.image(home_icon, x=icon_nav_x, y=icon_nav_y, w=icon_size, h=icon_size, link=projects_link)
        pdf.image(todo_icon, x=icon_nav_x + 15, y=icon_nav_y, w=icon_size, h=icon_size, link=link_todo)
        pdf.image(people_icon, x=icon_nav_x + 30, y=icon_nav_y, w=icon_size, h=icon_size, link=link_people)
        pdf.image(notes_icon, x=icon_nav_x + 45, y=icon_nav_y, w=icon_size, h=icon_size, link=link_notes)

        # Add lined paper effect
        add_lined_page()

# Output the PDF to a file
pdf_output_path = "Project Notes Template.pdf"
pdf.output(pdf_output_path)

print(f"PDF generated: {pdf_output_path}")
