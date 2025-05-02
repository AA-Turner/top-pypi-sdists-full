#!/usr/bin/env python3
from .functions import (argparse,
                        Image,
                        os,
                        PyPDF2,
                        clean_text,
                        write_to_file)
from .ocr_utils import (preprocess_image,
                        convert_image_to_text)
def images_to_pdf(image_paths, output_pdf):
    if not image_paths:
        raise ValueError("No image files provided for conversion.")

    # Open the first image and convert to RGB if necessary
    first_image = Image.open(image_paths[0])
    if first_image.mode in ("RGBA", "P"):
        first_image = first_image.convert("RGB")

    # List to hold subsequent images
    image_list = []
    for img_path in image_paths[1:]:
        img = Image.open(img_path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        image_list.append(img)

    # Save all images into a single PDF file
    first_image.save(output_pdf, "PDF", resolution=100.0, save_all=True, append_images=image_list)
    print(f"PDF saved as: {output_pdf}")
def process_pdf(main_pdf_path: str, pdf_output_dir: str) -> None:
    """Process a PDF into pages, images, text, preprocessed images, preprocessed text, and cleaned preprocessed text."""
    # Get PDF filename without extension
    pdf_name = os.path.splitext(os.path.basename(main_pdf_path))[0]

    # Create subdirectories for this PDF
    pdf_pages_dir = os.path.join(pdf_output_dir, 'pdf_pages')
    os.makedirs(pdf_pages_dir, exist_ok=True)
    images_dir = os.path.join(pdf_output_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)
    text_dir = os.path.join(pdf_output_dir, 'text')
    os.makedirs(text_dir, exist_ok=True)
    cleaned_text_dir = os.path.join(text_dir, 'cleaned')
    os.makedirs(cleaned_text_dir, exist_ok=True)
    preprocessed_images_dir = os.path.join(pdf_output_dir, 'preprocessed_images')
    os.makedirs(preprocessed_images_dir, exist_ok=True)
    preprocessed_text_dir = os.path.join(pdf_output_dir, 'preprocessed_text')
    os.makedirs(preprocessed_text_dir, exist_ok=True)
    cleaned_preprocessed_text_dir = os.path.join(preprocessed_text_dir, 'cleaned')
    os.makedirs(cleaned_preprocessed_text_dir, exist_ok=True)
    

    pdf_reader = PyPDF2.PdfReader(main_pdf_path)
    num_pages = len(pdf_reader.pages)
    logging.info(f"Processing {pdf_name} with {num_pages} pages")

    for page_num in range(num_pages):
        
            # Split PDF into individual pages
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_num])
            filename = f"{pdf_name}_page_{page_num + 1}"
            basename_pdf= f"{filename}.pdf"
            basename_png= f"{filename}.png"
            preprocessed_basename_png = f"preprocessed_{basename_png}"
            basename_txt= f"{filename}.txt"
            cleaned_basename_txt = f"cleaned_{basename_txt}"
            preprocessed_basename_txt = f"preprocessed_{basename_txt}"
            preprocessed_cleaned_basename_txt = f"preprocessed_cleaned_{basename_txt}"
            page_path = os.path.join(pdf_pages_dir, basename_pdf)
            with open(page_path, 'wb') as f:
                pdf_writer.write(f)

            # Convert PDF page to image
            images = convert_from_path(page_path)
            if images:
                # Save the image
                img_path = os.path.join(images_dir, basename_png)
                images[0].save(img_path, 'PNG')

                # Extract text directly from the image
                text = convert_image_to_text(img_path)
                txt_path = os.path.join(text_dir, basename_txt)
                write_to_file(file_path=txt_path, contents=text)

                # Clean the extracted text
                cleaned_text = clean_text(text)
                cleaned_text_path = os.path.join(cleaned_text_dir, cleaned_basename_txt)
                write_to_file(file_path=cleaned_text_path, contents=cleaned_text)

                # Preprocess the image
                
                preprocessed_img_path = os.path.join(preprocessed_images_dir, preprocessed_basename_png)
                preprocess_image(img_path, preprocessed_img_path)

                # Extract text from the preprocessed image
                preprocessed_text = convert_image_to_text(preprocessed_img_path)
                
                preprocessed_txt_path = os.path.join(preprocessed_text_dir, preprocessed_basename_txt)
                write_to_file(file_path=preprocessed_txt_path, contents=preprocessed_text)

                # Clean the preprocessed text
                preprocessed_cleaned_text = clean_text(preprocessed_text)
                
                preprocessed_cleaned_txt_path = os.path.join(cleaned_preprocessed_text_dir, preprocessed_cleaned_basename_txt)
                write_to_file(file_path=preprocessed_cleaned_txt_path, contents=preprocessed_cleaned_text)
                    
                logging.info(f"Processed page {page_num + 1} of {pdf_name}")
