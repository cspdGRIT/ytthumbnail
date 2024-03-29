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

def calculate_image_clarity(thumbnail_path):
    # Load the image using OpenCV
    image = cv2.imread(thumbnail_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Compute the Laplacian of the image to measure edge intensity
    laplacian = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Normalize the Laplacian score to range [0, 1]
    image_clarity_score = laplacian / 1000.0  # Adjust divisor as needed

    return image_clarity_score

# Function to calculate text readability score
def calculate_text_readability(thumbnail_path):
    # Use Pytesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(Image.open(thumbnail_path))

    # Dummy implementation: Calculate readability based on average word length
    word_lengths = [len(word) for word in extracted_text.split()]
    average_word_length = sum(word_lengths) / len(word_lengths)
    
    # Normalize the average word length to range [0, 1]
    text_readability_score = 1 - (average_word_length / 10)  # Assuming average word length around 5-6
    
    return text_readability_score

# Function to calculate color scheme score
def calculate_color_scheme(thumbnail_path):
    # Load the image using PIL
    image = Image.open(thumbnail_path)

    # Convert image to LAB color space
    lab_image = color.rgb2lab(image)

    # Perform segmentation using SLIC algorithm
    segments = segmentation.slic(np.array(image), n_segments=10)

    # Compute average color distance within each segment
    segment_colors = []
    for segment_id in np.unique(segments):
        segment_mask = (segments == segment_id)
        segment_lab = lab_image[segment_mask]
        segment_mean_lab = np.mean(segment_lab, axis=0)
        segment_colors.append(segment_mean_lab)
    
    # Calculate the color deviation as the standard deviation of LAB color values
    color_deviation = np.std(np.array(segment_colors), axis=0)
    
    # Normalize color deviation to range [0, 1] for each channel
    normalized_color_deviation = color_deviation / [100, 128, 128]  # Adjust divisor as needed

    # Compute the overall color scheme score as the average deviation across channels
    color_scheme_score = np.mean(normalized_color_deviation)

    return color_scheme_score

# Function to calculate composition score
def calculate_composition_score(thumbnail_path):
    # Dummy implementation
    # Example: Score based on rule of thirds
    # Load the image using PIL
    image = Image.open(thumbnail_path)

    # Calculate the dimensions of the image
    width, height = image.size

    # Calculate the coordinates for the thirds of the image
    third_width = width / 3
    third_height = height / 3

    # Check if the main subject is positioned in the center third of the image
    subject_position = (0.5 * width, 0.5 * height)  # Assume subject's center coordinates
    if third_width < subject_position[0] < 2 * third_width and third_height < subject_position[1] < 2 * third_height:
        composition_score = 1.0  # Subject is positioned in the center third
    else:
        composition_score = 0.5  # Subject is not centered

    return composition_score

# Function to calculate branding score
def calculate_branding_score(thumbnail_path):
    # Dummy implementation
    # Example: Score based on presence of logo or brand colors
    # Load the image using PIL
    image = Image.open(thumbnail_path)

    # Detect if the logo is present in the image (replace with your logo detection logic)
    logo_present = False  # Dummy value, replace with actual detection logic

    # Calculate branding score based on logo presence
    branding_score = 1.0 if logo_present else 0.0

    return branding_score

# Function to calculate emotion score
def calculate_emotion_score(thumbnail_path):
    # Dummy implementation
    # Example: Score based on facial expressions or color psychology
    # Load the image using PIL
    image = Image.open(thumbnail_path)

    # Analyze facial expressions or colors to determine emotion score (replace with actual emotion analysis logic)
    emotion_score = 0.8  # Dummy value, replace with actual analysis

    return emotion_score

# Function to calculate relevance score
def calculate_relevance_score(thumbnail_path):
    # Dummy implementation
    # Example: Score based on similarity between thumbnail content and video script
    # Load the image using PIL
    image = Image.open(thumbnail_path)

    # Analyze content of thumbnail and compare with video script to determine relevance score (replace with actual comparison logic)
    relevance_score = 0.9  # Dummy value, replace with actual analysis

    return relevance_score

# Function to predict click-through rate (CTR)
def predict_ctr(thumbnail_path):
    image = Image.open(thumbnail_path)

    # Extract image features (replace with feature extraction logic)
    image_features = [1.0, 0.5, 0.8]  # Dummy features, replace with actual extraction

    # Use machine learning model to predict CTR (replace with actual model prediction)
    ctr_prediction = sum(image_features) / len(image_features)

    return ctr_prediction

def score_thumbnail(thumbnail_path):
    # Dummy implementation - Replace with actual scoring mechanism
    # Example: Composite score based on composition, branding, emotion, relevance, and CTR prediction
    image_clarity_score = calculate_image_clarity(thumbnail_path)
    text_readability_score = calculate_text_readability(thumbnail_path)
    color_scheme_score = calculate_color_scheme(thumbnail_path)
    composition_score = calculate_composition_score(thumbnail_path)
    branding_score = calculate_branding_score(thumbnail_path)
    emotion_score = calculate_emotion_score(thumbnail_path)
    relevance_score = calculate_relevance_score(thumbnail_path)
    ctr_prediction_score = predict_ctr(thumbnail_path)

    # Combine scores with weights
    total_score = image_clarity_score+text_readability_score+color_scheme_score+composition_score+branding_score + emotion_score + relevance_score + ctr_prediction_score
    return total_score

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