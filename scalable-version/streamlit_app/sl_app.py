import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap

def get_font_size(image_width, image_height, text_length):
    base_font_size = 100  # Base font size
    max_font_size = 200  # Maximum font size
    min_text_ratio = 0.1  # Minimum text-to-image ratio
    max_text_ratio = 0.8  # Maximum text-to-image ratio
    
    text_ratio = text_length / (image_width * image_height)
    font_size = min(max_font_size, max(base_font_size, int(image_width * image_height * text_ratio * 0.8)))
    return font_size

# Function to generate YouTube thumbnail
def generate_thumbnail(video_description, logo_image_path):
    # Example video description text
    video_description = "A scenic mountain landscape with a flowing river."

    # Step 1: Text Preprocessing (if necessary)

    # Step 2: Generate descriptive caption using language model (e.g., GPT-3 or BERT)
    # generated_caption = generate_caption_with_lang_model(video_description)
    generated_caption = "car on top of a hill peak! car on top of a hill peak! car on top of a hill peak! car on top of a hill peak! "

    # Step 3: Retrieve background image using Unsplash API
    unsplash_access_key = "YYGSA1dBC_gOUsn30HEaDi07BVjj4o3Z5o_PcN3jTw4"
    query = generated_caption  # Use the generated caption as the query
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={unsplash_access_key}"
    response = requests.get(url)
    background_image_url = response.json()["urls"]["regular"]

    # Step 4: Download and compose background image
    background_image_response = requests.get(background_image_url)
    background_image = Image.open(BytesIO(background_image_response.content))
    
    # Step 5: Create new image with background size
    thumbnail_width = 1280
    thumbnail_height = 720
    thumbnail = Image.new("RGB", (thumbnail_width, thumbnail_height), color="white")

    # Step 6: Resize background image to fit thumbnail
    background_width, background_height = background_image.size
    background_image = background_image.resize((thumbnail_width, thumbnail_height))
    # thumbnail_width, thumbnail_height = background_image.size
    thumbnail.paste(background_image, (0, 0))
    # Step 5: Overlay caption text on the background image
    caption_text = generated_caption
    # font = ImageFont.load_default()  # You can use a custom font if needed
    url_font_goog = "https://fonts.googleapis.com/css2?family=Roboto:wght@900&display=swap"
    # font_path="pictory/thumbnail-maker/budmo-jiggler.otf"
    font_path="/Users/cspd/Documents/work_learn/pictory/thumbnail-maker/fonts/Poppins-Bold.ttf"
    # font_size = 100
    # font = ImageFont.truetype(font_path, font_size)
    font = ImageFont.truetype(font_path, size=get_font_size(thumbnail_width, thumbnail_height, len(caption_text)))

    max_caption_width = thumbnail_width - 40  # Leave some padding on both sides
    font_size = 100
    font = ImageFont.truetype(font_path, size=font_size)

    draw = ImageDraw.Draw(background_image)

    # Step 11: Reduce font size until text fits within max width for each line
    # wrapped_text = textwrap.fill(caption_text, width=20)  # Adjust width as needed
    # wrapped_lines = wrapped_text.split("\n")

    max_chars_per_line = 25
    wrapped_lines = [caption_text[i:i+max_chars_per_line] for i in range(0, len(caption_text), max_chars_per_line)]
    line_y = (thumbnail_height - len(wrapped_lines) * font_size) // 2  # Calculate vertical position

    for line in wrapped_lines:
        # Adjust font size until text fits within max width
        while font.getsize(line)[0] > max_caption_width:
            font_size -= 1
            font = ImageFont.truetype(font_path, size=font_size)

        # Draw caption text on thumbnail
        text_width, text_height = draw.textsize(line, font=font)
        x_position = (thumbnail_width - text_width) // 2  # Center horizontally
        draw.text((x_position, line_y), line, fill="white", font=font)

        # Move to next line
        line_y += text_height
    return background_image

# Streamlit app
def main():
    st.title("Pictory - YT thumbnail gen")

    # Input fields
    video_description = st.text_area("Video Description", "Enter your video description here")
    logo_image_path = st.file_uploader("Upload Logo Image (PNG or JPEG)", type=["png", "jpg", "jpeg"])

    # Generate thumbnail on button click
    if st.button("Generate Thumbnail"):
        if not video_description:
            st.warning("Please enter a video description")
        elif not logo_image_path:
            # st.warning("Please upload a logo image")
            pass
        else:
            # Generate thumbnail
            thumbnail = generate_thumbnail(video_description, logo_image_path)
            # thumbnail.show()
            # Display thumbnail
            st.image(thumbnail, caption="Generated Thumbnail", use_column_width=True)

# Run the app
if __name__ == "__main__":
    main()