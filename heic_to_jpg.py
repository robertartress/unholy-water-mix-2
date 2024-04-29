import os
from PIL import Image
import pyheif

def convert_heic_to_jpg(heic_path, output_folder):
    # Read the HEIC file
    heif_file = pyheif.read(heic_path)
    
    # Convert to an Image object
    image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    
    # Define the output path
    base_name = os.path.basename(heic_path)
    file_name = os.path.splitext(base_name)[0] + '.jpg'
    output_path = os.path.join(output_folder, file_name)
    
    # Save the image as JPEG
    image.save(output_path, "JPEG")

    print(f"Converted {heic_path} to {output_path}")

# Example usage
input_heic = "./album_art.heic"
output_dir = "./"
convert_heic_to_jpg(input_heic, output_dir)
