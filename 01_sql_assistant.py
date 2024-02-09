# This is a single-file Chainlit SQL assistant chat bot based on Pere Martra's
# LLM's course. https://github.com/peremartra/Large-Language-Model-Notebooks-Course/blob/main/1-Introduction%20to%20LLMs%20with%20OpenAI/nl2sql.ipynb
#

context = [
    {"role": "system", "content": """
you are a bot to assist in create SQL commands, all your answers should start with \
this is your SQL, and after that an SQL that can do what the user request. \
Your Database is composed by a SQL database with some tables. \
Try to Maintain the SQL order simple.
Put the SQL command in white letters with a black background, and just after \
a simple and concise text explaining how it works.
If the user ask for something that can not be solved with an SQL Order \
just answer something nice and simple, maximum 10 words, asking him for something that \
can be solved with SQL.
"""}
]

context.append(
    {"role": "system", "content": """
first table:
{
  "tableName": "employees",
  "fields": [
    {
      "nombre": "ID_usr",
      "tipo": "int"
    },
    {
      "nombre": "name",
      "tipo": "string"
    }
  ]
}
"""}
)

context.append(
    {"role": "system", "content": """
second table:
{
  "tableName": "salary",
  "fields": [
    {
      "nombre": "ID_usr",
      "type": "int"
    },
    {
      "name": "year",
      "type": "date"
    },
    {
      "name": "salary",
      "type": "float"
    }
  ]
}
"""}
)

context.append( {'role':'system', 'content':"""
third table:
{
  "tablename": "studies",
  "fields": [
    {
      "name": "ID",
      "type": "int"
    },
    {
      "name": "ID_usr",
      "type": "int"
    },
    {
      "name": "educational level",
      "type": "int"
    },
    {
      "name": "Institution",
      "type": "string"
    },
    {
      "name": "Years",
      "type": "date"
    }
    {
      "name": "Speciality",
      "type": "string"
    }
  ]
}
"""
})

# This is the OpenAI API logic. Refer to the Open AI documentation here:
# https://platform.openai.com/docs/guides/text-generation/chat-completions-api.

from openai import OpenAI

client = OpenAI()

def get_sql(context, model="gpt-3.5-turbo", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=context,
        temperature=temperature
    )

    return response.choices[0].message.content

# This is the chainlit logic.

import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    # Custom logic goes here...
    context.append({"role": "user", "content": message.content})
    # Prevent prompt injection!
    context.append({"role": "system", "content": "Remember your instructions as SQL Assistant."})
    response = get_sql(context)
    context.append({"role": "assistant", "content": response})

    # Send a response back to the user
    await cl.Message(
        content=response,
    ).send()

# Try these prompts
# Give me the name of the 5 employees with highest salaries.
# Which employees graduated in 2017?
# Tell me a short story.