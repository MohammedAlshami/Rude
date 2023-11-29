from flask import Flask, render_template, request
import json
from openai import OpenAI
client = OpenAI(api_key="API_KEY")


app = Flask(__name__, template_folder='templates')

# In-memory chat history (you might want to use a database in a real application)
chat_history = []


history = []
def rude_guy(message):
    # adding to history
    history.append({"role": "system", "content": "Marv is a rude chatbot that is also blunt."})
    history.append({"role": "user", "content": message})

    # Processing the history and new message
    response = client.chat.completions.create(
      model="ft:gpt-3.5-turbo-0613:personal::8Q2Iphac",
      messages=history
    )

    # getting the response
    response_msg = response.choices[0].message.content

    # adding the response to thec history
    history.append({"role": "system", "content": response_msg})

    # returning the response to the user
    return response_msg
    

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_message = request.form['user_message']
        # Process user input (You can replace this logic with your own chatbot logic)
        assistant_response = rude_guy(user_message)
        # Update chat history
        chat_history.append({'role': 'user', 'content': user_message})
        chat_history.append({'role': 'assistant', 'content': assistant_response})

    return render_template('home.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
