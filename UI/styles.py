color_palette = {
    "navy_blue": "#0d1b2a",
    "white": "#ffffff",
    "baby_blue": "#A9D6E5",
    "lighter_blue": "#F8F9FA",
    "dark_navy": "#1b263b"
}

def load_css():
    return f"""
        <style>
        .stApp {{
            background-color: {color_palette['navy_blue']}; /* Navy blue background */
        }}
        .card {{
            background-color: {color_palette['white']}; /* White card background */
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow for modern look */
        }}
        .section-header {{
            color: {color_palette['baby_blue']}; /* Baby blue header color */
            text-align: center;
            font-size: 2.2em;
            margin-bottom: 10px;
        }}
        .sub-header {{
            color: {color_palette['baby_blue']}; /* Lighter blue for sub-headers */
            font-size: 1.2em;
            text-align: center;
        }}
        .st-emotion-cache-9ycgxx {{
            color: {color_palette['baby_blue']} !important; /* Drag and drop files here text color */
        }}
        .st-emotion-cache-1aehpvj {{
            color: {color_palette['baby_blue']} !important; /* Limit 200MB per file • PDF text color */
        }}
        /* Change button background and text color */
        button.st-emotion-cache-7ym5gk {{
            background-color: {color_palette['navy_blue']} !important; /* Button background color */
            color: {color_palette['white']} !important; /* Button text color */
            border: none; /* Remove border */
            border-radius: 10px; /* Optional: Adjust border radius */
            padding: 10px 20px; /* Optional: Add padding */
        }}
        button.st-emotion-cache-7ym5gk:hover {{
            background-color: {color_palette['baby_blue']} !important; /* Button hover background color */
            color: {color_palette['navy_blue']} !important; /* Button hover text color */
        }}
        [data-testid="stSidebarContent"]{{
             background-color: {color_palette['baby_blue']};
            border: 2px solid white; /* black border, 2px thick */
            border-radius: 5px; /* opti
        }}
        /* Style for the + and - buttons */
        .st-emotion-cache-76z9jo.e116k4er2 button {{
            color: {color_palette['navy_blue']}; /* navy blue text color for + and - buttons */
        }}
        /* Hover effect for the + and - buttons */
        .st-emotion-cache-76z9jo.e116k4er2 button:hover {{
            background-color: {color_palette['navy_blue']}; /* Baby blue background on hover */
            color: {color_palette['white']}; 
        }}
        h1, h2,h3, h4 {{
            color: {color_palette['lighter_blue']}; /* Main text color (white) */
        }}
        div .card {{
            color: {color_palette['navy_blue']}; /* Main text color (white) */
        }}
        hr {{
            border: 1px solid {color_palette['baby_blue']}; /* Baby blue horizontal divider */
        }}
        .stSidebar {{
            background-color: {color_palette['dark_navy']} !important; /* Dark navy sidebar background */
        }}
        .stSidebar div, .stSidebar label,p {{
            color: {color_palette['baby_blue']} !important; /* Baby blue text in sidebar */
        }}
        .st-emotion-cache-16idsys e1nzilvr5
        header {{
            background-color: {color_palette['navy_blue']} !important; /* Dark navy for the top title bar */
            color: {color_palette['baby_blue']} !important; /* Baby blue for the title text */
        }}
        .st-emotion-cache-16idsys.e1nzilvr5 > p {{
            color: {color_palette['white']}; 
        }}
        footer {{
            background-color: {color_palette['baby_blue']}; /* Baby blue footer */
            color: {color_palette['navy_blue']}; /* Navy text for footer */
            padding: 10px;
            text-align: center;
        }}
        </style>
    """

