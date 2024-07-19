from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import google.generativeai as genai
import re
import requests

load_dotenv()

#os.environ['GOOGLE_API_KEY'] = ""
#genai.configure(api_key = os.environ['GOOGLE_API_KEY'])
genai.configure(api_key = os.environ.get('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-1.5-flash')
#model = genai.GenerativeModel('gemini-pro')

def remove_text_after_role_model(input_string):
    # Split the string by '"role": "model"' and take the first part
    parts = input_string.split('"role": "model"', 1)
    return parts[0]

def remove_first_n_characters(input_string, n):
    return input_string[n:]

def remove_last_n_characters(input_string):
    return input_string[:-35]
    
def remove_spaces_from_line(line):
    return line.strip()

def replace_double_newline_with_br_tags(input_string):
    return input_string.replace('\\n', '<br/>')

def replace_double_star_with_b_tags(input_string):
    return input_string.replace('**', '<b>')

def convert_to_bold(input_string):
  return re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', input_string)

def replace_triple_slash_to_single(input_string):
    return input_string.replace('\\\"', '\"')

app= Flask(__name__)


@app.route('/')
def home():
    
    return render_template('index.html')

@app.route('/dat', methods=['POST'])
def dat():

    inputRequest = request.form['user_input']
    response = model.generate_content(inputRequest)
   
    newResponse = response
    res2 = str(newResponse)
    index = res2.find('"text":')

    if index != -1:
        result = res2[index:]
        result = remove_first_n_characters(result, 9)
        result = remove_text_after_role_model(result)
        result = remove_spaces_from_line(result)
        result = remove_last_n_characters(result)
        result = replace_double_newline_with_br_tags(result)
        result = convert_to_bold(result)
        result = replace_triple_slash_to_single(result)
        
     
    return render_template('index.html', response_data='{}'.format(result))


# Define a route for your API endpoint
@app.route('/api/generate', methods=['POST'])
def post_generate():
    headersToken = os.environ.get('HEADER_TOKEN')
    auth_header = request.headers.get('Authorization')
    
    if auth_header == headersToken:
        inputRequest = request.form['content']
        response = model.generate_content(inputRequest)
        newResponse = response
        res2 = str(newResponse)
        index = res2.find('"text":')

        if index != -1:
            result = res2[index:]
            result = remove_first_n_characters(result, 9)
            result = remove_text_after_role_model(result)
            result = remove_spaces_from_line(result)
            result = remove_last_n_characters(result)
            result = replace_double_newline_with_br_tags(result)
            result = convert_to_bold(result)
            result = replace_triple_slash_to_single(result)
       
        output = {
            "message": result,
            "status": 200
        }
       
        return jsonify(output)
    else:
        output = {
            "message": 'Invalid Token',
            "status": 400
        }
        return jsonify(output)


# Define a route for your API endpoint for test 
@app.route('/api/test', methods=['POST'])
def post_test():

    headersToken = os.environ.get('HEADER_TOKEN')
    auth_header = request.headers.get('Authorization')
    
    if auth_header == headersToken:
        message = "The term \\\"Planet B\\\" has a few different meanings, depending on the context:<br/><br/><b>1. A Hypothetical Second Home:</b><br/><br/>* In the context of climate change and potential existential threats, \\\"Planet B\\\" is often used as a <b>metaphor for a backup plan</b> \– a second planet where humanity could relocate if Earth becomes uninhabitable. <br/>* This is a <b>highly speculative and improbable scenario</b>, as finding and colonizing another planet suitable for human life is a monumental challenge.<br/>* The phrase often serves as a <b>cautionary reminder</b> of the urgency to address climate change and protect Earth.<br/><br/><b>2. A Specific Planet:</b><br/><br/>* In the context of <b>exoplanet discovery</b>, \\\"Planet B\\\" can refer to a <b>specific planet orbiting another star</b>. <br/>* This might be a real planet that has been identified through astronomical observations, or it might be a <b>hypothetical planet</b> that scientists believe could exist based on theoretical models.<br/><br/><b>3. A Concept in Science Fiction:</b><br/><br/>* \\\"Planet B\\\" can also appear in <b>science fiction literature and movies</b> as the name of a specific planet with unique characteristics.<br/>* These fictional planets might be inhabited by alien species, have advanced technology, or possess fantastical landscapes.<br/><br/><b>To understand the meaning of \\\"Planet B\\\" in a specific context, you need to consider the source and the surrounding information.</b><br/><br/>If you have a specific instance in mind where you encountered this phrase, please provide more context and I can give you a more specific answer."

        message = replace_double_newline_with_br_tags(message)
        message = convert_to_bold(message)
        message = replace_triple_slash_to_single(message)
       
        output = {
            "message": message,
            "status": 200
        }
        
        return jsonify(output)
    else:
        output = {
            "message": 'Invalid Token',
            "status": 400
        }
        return jsonify(output)


if __name__ == '__main__':
   app.run(debug=True)