from pathlib import Path
from datetime import datetime

# from io import BytesIO
# from barcode import Code128
# from barcode.writer import ImageWriter

BASE_DIR = Path(__file__).resolve().parent.parent


def send_email(subject, body, receiver_email, media=False, media_path=None):
    import smtplib
    import ssl
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email import encoders

    import os

    sender_email = os.environ.get("EMAIL_USER")
    receiver_email = receiver_email
    password = os.environ.get("EMAIL_PASS")
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    media_path = BASE_DIR / "media" /  media_path
    print(media_path)

    html = f"""\
    <html>
    <body>
        <p>{body}<br><br>

    Regrads,<br>
    Youth Club
            </p>
        </body>
        </html>
    """

    part2 = MIMEText(html, "html")

        # Attach the file
    if media:
        attachment = open(media_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename= ' + str(media_path))
        message.attach(part)

    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(os.environ.get("SMTP_HOST"), os.environ.get("SMTP_PORT"), context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


def generate_ticket(event_id, sno, ticket_featured_photo_path, name, phone, response_id):
    from PIL import Image, ImageDraw, ImageFont

    import qrcode

    organization_logo_path = BASE_DIR / "static/yc-logo.jpg"

    output_image_path  = f"uploads/event_{event_id}/ticket_{response_id}_.jpg"
    saving_path  = BASE_DIR / f"media/uploads/event_{event_id}/ticket_{response_id}_.jpg"

    width, height = 768, 1300
    ticket_image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(ticket_image)

    # if not sample:
        # find_real_path = ticket_featured_photo_path.find("uploads/")
        # ticket_featured_photo_path = ticket_featured_photo_path[find_real_path:]
        # ticket_featured_photo_path = str(BASE_DIR /  ticket_featured_photo_path)


    ticket_featured_photo = Image.open(ticket_featured_photo_path)

    # Define the new size (width, height)
    new_size = (768, 384)

    # Resize the original image
    resized_image = ticket_featured_photo.resize(new_size)

    # Specify the position where you want to paste the resized image
    position = (0, 0)

    # Paste the resized image onto the original image
    ticket_image.paste(resized_image, position)

    fontsize = 40
    headingfontsize = 52

    headingfont = ImageFont.truetype(str(BASE_DIR / "static/Raleway_600SemiBold.ttf"), headingfontsize)
    oswaldBold = ImageFont.truetype(str(BASE_DIR / "static/Oswald-SemiBold.ttf"), fontsize)
    oswaldLight = ImageFont.truetype(str(BASE_DIR / "static/Oswald-Light.ttf"), fontsize)

    # Draw organization logo
    logo = Image.open(organization_logo_path)
    logo = logo.resize((78, 78))
    ticket_image.paste(logo, (30, 420))

    now = datetime.now()

    current_date = now.strftime("%Y-%m-%d")  # Year-month-day format
    current_hour = now.strftime("%H")  # Hour (00-23)
    current_minute = now.strftime("%M")

    # Draw event details
    # Generate barcode
    encoding_code = str(event_id)
    barcode_value = f"YC{encoding_code}{response_id}"
    # barcode_bytes = BytesIO()
    # barcode = Code128(barcode_value, writer=ImageWriter())
    # barcode.default_writer_options['write_text'] = False

    # barcode.write(barcode_bytes)

    # # Move BytesIO cursor to the beginning
    # barcode_bytes.seek(0)

    # # Paste barcode onto the ticket
    # barcode_image = Image.open(barcode_bytes)

    qr = qrcode.QRCode(box_size=2)
    qr.add_data(barcode_value)
    qr.make()
    img_qr = qr.make_image()

    newSize = (440, 440) # new size will be 500 by 300 pixels, for example
    resized = img_qr.resize(newSize, resample=Image.NEAREST)
    ticket_image.paste(resized, (340, 850))

    # Save the image

    draw.text((140, 430), f"Youth Club", fill="black", font=headingfont)

    # Draw user information
    draw.text((440, 540), f"SNO: {sno}", fill="black", font=oswaldBold)
    draw.text((30, 540), "YOUR NAME: ", fill="black", font=oswaldLight)
    draw.text((30, 600), f"{name}".upper(), fill="black", font=oswaldBold)
    draw.text((30, 680), "YOUR PHONE: ".upper(), fill="black", font=oswaldLight)
    draw.text((30, 740), f"{phone}".upper(), fill="black", font=oswaldBold)

    draw.text((30, 820), f"ISSUED AT: {current_date}, {current_hour}:{current_minute}", fill="black", font=oswaldLight)
    ticket_image.save(saving_path)

    return output_image_path, barcode_value
