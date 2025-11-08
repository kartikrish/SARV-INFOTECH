import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, add
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import os
import sys
from pickle import load
import string

# --- Define Constants (MUST be set based on your pre-processed dataset) ---
# NOTE: These values are typical for the Flickr8k dataset but MUST match your data.
MAX_LENGTH = 34      
VOCAB_SIZE = 7057
EMBEDDING_DIM = 256
FEATURE_DIM = 4096   # Output dimension of the VGG16 'fc2' layer

# --- 1. CNN Encoder (Feature Extractor) Setup ---
def setup_vgg_encoder():
    """Initializes and configures the VGG16 model for feature extraction."""
    # Load VGG16 pre-trained on ImageNet
    vgg_model = VGG16()
    # Re-structure the model to remove the final classification layers (Softmax/Dense)
    # We use the output of the second-to-last layer ('fc2'), which is a 4096-dim vector.
    vgg_model = Model(inputs=vgg_model.inputs, outputs=vgg_model.layers[-2].output)
    return vgg_model

def extract_vgg_features(image_path, model):
    """Extracts features for a single image."""
    try:
        img = load_img(image_path, target_size=(224, 224))
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        feature = model.predict(img, verbose=0)
        return feature
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

# --- 2. RNN Decoder (Caption Generator) Architecture ---
def define_captioning_model(vocab_size, max_length, feature_dim, embedding_dim):
    """Defines the Encoder-Decoder LSTM model architecture."""
    # Image Feature Input (Encoder Output)
    image_input = Input(shape=(feature_dim,), name='image_input')
    fe1 = Dropout(0.5)(image_input)
    # Map the 4096-dim feature vector to the smaller embedding space
    fe2 = Dense(embedding_dim, activation='relu')(fe1)

    # Sequence Input (Partial Caption)
    caption_input = Input(shape=(max_length,), name='caption_input')
    # Word Embedding Layer
    se1 = Embedding(vocab_size, embedding_dim, mask_zero=True)(caption_input)
    se2 = Dropout(0.5)(se1)
    # LSTM Layer
    se3 = LSTM(embedding_dim)(se2)

    # Decoder Merger and Output
    # Merge the image feature and the sequence output
    decoder1 = add([fe2, se3])
    decoder2 = Dense(embedding_dim, activation='relu')(decoder1)
    # Softmax output layer predicts the probability of the next word
    outputs = Dense(vocab_size, activation='softmax')(decoder2)

    # Define the final model
    model = Model(inputs=[image_input, caption_input], outputs=outputs)
    return model

# --- 3. Inference / Caption Generation Logic (Greedy Search) ---
def word_for_id(integer, tokenizer):
    """Maps an integer to its corresponding word in the tokenizer vocabulary."""
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

def generate_caption(model, tokenizer, photo_features, max_length):
    """
    Generates a caption for the image features using Greedy Search.
    
    Args:
        model (Model): The trained Keras captioning model.
        tokenizer (Tokenizer): The fitted Keras Tokenizer object.
        photo_features (np.array): The 4096-dim feature vector of the image.
        max_length (int): The maximum length of the output caption.

    Returns:
        str: The generated, cleaned-up caption.
    """
    # Start the sequence with the 'startseq' token
    in_text = 'startseq'
    
    # Iterate until max length or end token
    for i in range(max_length):
        # Prepare the current sequence input
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length, padding='post')[0]
        
        # Predict the next word's probability distribution
        # The image features (1, 4096) and sequence (1, max_length) are the inputs
        yhat = model.predict([photo_features, np.array([sequence])], verbose=0)
        
        # Select the word with the highest probability (Greedy Search)
        yhat = np.argmax(yhat)
        
        # Map integer to word
        word = word_for_id(yhat, tokenizer)
        
        if word is None:
            break
            
        in_text += ' ' + word
        
        if word == 'endseq':
            break

    # Clean up and return the caption
    final_caption = in_text.split()
    # Remove 'startseq' and 'endseq'
    final_caption = final_caption[1:-1]
    final_caption = ' '.join(final_caption)
    
    return final_caption

# --- 4. Main Execution Block (Setup and Dummy Run) ---
if __name__ == '__main__':
    # --- IMPORTANT SETUP: Replace these with your actual file paths ---
    # 1. Path to your saved trained model weights
    MODEL_PATH = 'path/to/your/trained_captioning_model.h5' 
    # 2. Path to your saved Keras Tokenizer object
    TOKENIZER_PATH = 'path/to/your/tokenizer.pkl'
    # 3. Path to the image you want to caption
    TEST_IMAGE_PATH = 'path/to/your/test_image.jpg'
    
    print("--- Image Captioning AI Setup ---")
    
    # 1. Initialize VGG16 Encoder
    vgg_encoder = setup_vgg_encoder()
    print("VGG16 Encoder (Feature Extractor) Ready.")
    
    # 2. Define Captioning Model Architecture
    caption_model = define_captioning_model(VOCAB_SIZE, MAX_LENGTH, FEATURE_DIM, EMBEDDING_DIM)
    
    # --- LOAD ARTIFACTS (CRITICAL STEP) ---
    try:
        # Load trained weights into the model
        caption_model.load_weights(MODEL_PATH)
        print(f"Model weights loaded successfully from: {MODEL_PATH}")
        
        # Load the fitted tokenizer
        with open(TOKENIZER_PATH, 'rb') as f:
            tokenizer = load(f)
        print(f"Tokenizer loaded successfully from: {TOKENIZER_PATH}")

    except FileNotFoundError:
        print("\nFATAL ERROR: Model weights or Tokenizer not found!")
        print(f"Please train your model and update MODEL_PATH ('{MODEL_PATH}') and TOKENIZER_PATH ('{TOKENIZER_PATH}') with the correct file locations.")
        sys.exit(1)
        
    # --- RUN INFERENCE ---
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"\nFATAL ERROR: Test image not found at: {TEST_IMAGE_PATH}")
        sys.exit(1)

    print(f"\n--- Running Inference on: {TEST_IMAGE_PATH} ---")
    
    # Extract features from the test image
    test_features = extract_vgg_features(TEST_IMAGE_PATH, vgg_encoder)
    
    if test_features is not None:
        # Generate the caption
        generated_caption = generate_caption(caption_model, tokenizer, test_features, MAX_LENGTH)
        
        print("\n==============================================")
        print(f"Image: {os.path.basename(TEST_IMAGE_PATH)}")
        print(f"Generated Caption: {generated_caption}")
        print("==============================================")