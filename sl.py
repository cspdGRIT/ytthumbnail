import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap
from transformers import pipeline
from spacy.lang.en.stop_words import STOP_WORDS

import spacy

# Load the English language model
# nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("en_core_web_lg")

def get_first_7_words(sentence):
    # Split the sentence into words
    words = sentence.split()
    first_7_words = ""

    for i,word in enumerate(words):
        if i==6 and word in STOP_WORDS:
            break
        first_7_words+=' '+word
        if len(first_7_words.split())>=7:
            break
    
    return first_7_words.rstrip()+" ..."
    # # Take the first 7 words
    # if words[7] not in STOP_WORDS:
    #     first_7_words = ' '.join(words[:7])
    # else:
    #     first_7_words = ' '.join(words[:6])
    # return first_7_words

def generate_thumbnail_caption(video_description):
    # Preprocess the text (optional)
    video_description = video_description.lower()  # Convert to lowercase
    # Other preprocessing steps can be added as needed

    # Perform part-of-speech tagging and named entity recognition
    doc = nlp(video_description)

    # Extract relevant entities and keywords
    entities = [ent.text for ent in doc.ents]  # Extract named entities
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN", "ADJ"]]  # Extract nouns, proper nouns, and adjectives

    # Combine entities and keywords to form the thumbnail caption text
    thumbnail_caption_1 = " ".join(entities + keywords)

    # Load the text generation pipeline with a pre-trained GPT-2 model
    text_generator = pipeline("text-generation", model="gpt2")

    # Generate caption for the video description
    thumbnail_caption_2 = text_generator(video_description, max_length=20, num_return_sequences=1)[0]['generated_text']
    doc_desc = nlp(video_description)

    doc_1 = nlp(thumbnail_caption_1)
    doc_2= nlp(thumbnail_caption_2)
    score_1=doc_desc.similarity(doc_1)
    score_2=doc_desc.similarity(doc_2)
    print("thumbnail_caption_1:\t",thumbnail_caption_1,"\nscore:\t",score_1)
    print("thumbnail_caption_2:\t",thumbnail_caption_2,"\nscore:\t",score_2)
    
    thumbnail_caption=""

    if score_1>score_2:
        thumbnail_caption = thumbnail_caption_1
    else:
        thumbnail_caption = thumbnail_caption_2
    
    # # Process the text
    # doc = nlp(thumbnail_caption)
    
    # # Tokenize the sentences and get the first 7 words from each sentence
    # summarized_sentences = [str(sentence)[:7] for sentence in doc.sents]
    
    # # Join the summarized sentences into a single string
    # summarized_text = " ".join(summarized_sentences)
    return get_first_7_words(thumbnail_caption)

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

    # Step 1: Text Preprocessing (if necessary)

    # Step 2: Generate descriptive caption using language model (e.g., GPT-3 or BERT)
    # generated_caption = generate_caption_with_lang_model(video_description)
    generated_caption = generate_thumbnail_caption(video_description)
    print("Generated Thumbnail Caption Text:")
    print("---------------------------------")
    print(generated_caption)

    # Step 3: Retrieve background image using Unsplash API
    unsplash_access_key = "YYGSA1dBC_gOUsn30HEaDi07BVjj4o3Z5o_PcN3jTw4"
    query = generated_caption  # Use the generated caption as the query
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={unsplash_access_key}"
    response = requests.get(url)
    background_image_url = response.json()["urls"]["regular"]

    # Step 4: Download and compose background image
    background_image_response = requests.get(background_image_url)
    background_image = Image.open(BytesIO(background_image_response.content))
    logo_image = Image.open(logo_image_path)
    
    # Step 5: Create new image with background size
    thumbnail_width = 1280
    thumbnail_height = 720
    thumbnail = Image.new("RGB", (thumbnail_width, thumbnail_height), color="white")

    
    # Step 8: Add logo to thumbnail
    logo_width, logo_height = logo_image.size
    # logo_position = (thumbnail_width - logo_width - 20, thumbnail_height - logo_height - 20)
    logo_position = (thumbnail_width - 100 -10,10)
    logo_image = logo_image.convert('RGBA')
    # mask.logo_image = mask.logo_image.convert('L')

    # thumbnail.paste(logo_image, logo_position)

    # Step 6: Resize background image to fit thumbnail
    background_width, background_height = background_image.size
    background_image = background_image.resize((thumbnail_width, thumbnail_height))
    # thumbnail_width, thumbnail_height = background_image.size
    logo_image = logo_image.resize((100, 100))
    background_image.paste(logo_image, logo_position)
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
            print("Video Description:")
            print("------------------")
            print(video_description)
            thumbnail = generate_thumbnail(video_description, logo_image_path)
            print("Generated Thumbnail:")
            print("---------------------------------")
            print(thumbnail)
            # thumbnail.show()
            # Display thumbnail
            st.image(thumbnail, caption="Generated Thumbnail", use_column_width=True)

# Run the app
if __name__ == "__main__":
    main()