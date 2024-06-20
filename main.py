import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait


LINKS = [
  "https://example.com/comics_name/",
]

TEMPORARY_FOLDER_PATH = "temp"
OUTPUT_FOLDER_PATH = "out"
OUTPUT_PDF_NAME = "output"



def init():
  # Create a temporary folder if it doesn't exist
  if not os.path.exists(TEMPORARY_FOLDER_PATH):
    os.makedirs(TEMPORARY_FOLDER_PATH)

  # Create an output folder if it doesn't exist
  if not os.path.exists(OUTPUT_FOLDER_PATH):
    os.makedirs(OUTPUT_FOLDER_PATH)
    
  print("Folders created.")


def extract_image_links(page_link):
  response = requests.get(page_link)
  soup = BeautifulSoup(response.text, 'html.parser')
  image_tags = soup.find_all('img')
  image_links = [tag['src'] for tag in image_tags]
  return image_links

def formatted_number(max_number, n):
    # Convert max_number and n to strings
    max_str = str(max_number)
    n_str = str(n)
    
    # Calculate the total length required for the string
    total_length = len(max_str)
    
    # Create the formatted string starting with '0' and ending with n_str
    formatted_str = '0' * (total_length - len(n_str)) + n_str
    
    return formatted_str

def clear_temporary_folder():
  for f in os.listdir(TEMPORARY_FOLDER_PATH):
    file_path = os.path.join(TEMPORARY_FOLDER_PATH, f)
    try:
      if os.path.isfile(file_path):
        os.unlink(file_path)
    except Exception as e:
      print(f"Failed to delete {file_path}: {e}")
  print("Temporary folder cleared.")


def download_images(image_links, begin=1):
  for i in range(begin, len(image_links)-begin):   
    try:
        # Send a GET request to the image URL
        img_response = requests.get(image_links[i], stream=True)
        img_response.raise_for_status()
        
        # Define the image path
        img_path = os.path.join(TEMPORARY_FOLDER_PATH, f"img_{formatted_number(len(image_links),i)}.jpg")
        
        # Save the image
        with open(img_path, 'wb') as img_file:
            for chunk in img_response.iter_content(1024):
                img_file.write(chunk)
                
        print(f"Image successfully downloaded: {img_path}")
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {image_links[i]}: {e}")
    

def images_to_pdf(folder_path, output_pdf_path):
  # Get a list of all image files in the directory
  img_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

  if not img_files:
    print("No images found in the directory.")
    return

  # Create a canvas to write the PDF
  c = canvas.Canvas(output_pdf_path)

  for img_file in img_files:
    img_path = os.path.join(folder_path, img_file)
    with Image.open(img_path) as img:
      # Ensure the image is in RGB mode
      if img.mode != 'RGB':
          img = img.convert('RGB')

      # Get the dimensions of the image
      img_width, img_height = img.size

      # Set the page size to the image size
      c.setPageSize(portrait((img_width, img_height)))
      
      # Draw the image on the canvas
      c.drawImage(img_path, 0, 0, img_width, img_height)

      # Add a new page for the next image
      c.showPage()
    
    print(f"Image added to PDF: {img_path}")

  # Save the PDF
  c.save()

  print(f"PDF created successfully at {output_pdf_path}")


def find_available_number():
  first_number_available = 0
  while (os.path.exists(os.path.join(OUTPUT_FOLDER_PATH, OUTPUT_PDF_NAME+"_"+formatted_number(len(LINKS),first_number_available)+".pdf"))):
    first_number_available += 1
  return first_number_available


def main():
  init()
  
  first_number_available = find_available_number()
  
  for i in range(first_number_available, len(LINKS)+first_number_available):
    image_links = extract_image_links(LINKS[i-first_number_available])
    clear_temporary_folder()
    download_images(image_links)
    
    images_to_pdf(TEMPORARY_FOLDER_PATH, os.path.join(OUTPUT_FOLDER_PATH, OUTPUT_PDF_NAME+"_"+formatted_number(len(LINKS),i)+".pdf"))
    print("\n \n")
  
  print("All PDFs created successfully.")


main()