from flask import Flask, render_template, request, send_file
from flask_pymongo import PyMongo
import gridfs
from rembg import remove
from PIL import Image
import io
import base64
app = Flask(__name__)
 
# Set up MongoDB connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/bgremover"
mongo = PyMongo(app)
fs = gridfs.GridFS(mongo.db)

@app.route('/', methods=['GET','POST'])
def home():
    output_image_data = None
    if request.method == 'POST':
        # Get the file from the form
        file = request.files['file']
        if file:
            #reads the uploaded file directly from memory wihtout loading it into disk
            input_image = Image.open(file.stream);
            #It pases the image to the rembg library to remove the background where it uses deep learning to remove the background
            #and returns the image with the background removed in png format
            output_image = remove(input_image)
            # Create a BytesIO object to hold the output image
            output_io = io.BytesIO()    
            output_image.save(output_io, format='PNG')
            # Move the cursor to the beginning of the BytesIO object, so it can be read from the start whem sending it or saving it
            output_io.seek(0)
            
            # Encode for HTML
            img_base64 = base64.b64encode(output_io.getvalue()).decode('utf-8')
            output_image_data = f"data:image/png;base64,{img_base64}"
            
        else:
            return 'No file uploaded.'
    return render_template('index.html', output_image_data=output_image_data)
        
    

if __name__ == '__main__':
    app.run(debug=True)