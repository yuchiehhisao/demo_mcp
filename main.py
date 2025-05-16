from openai import OpenAI
import base64
import os
import pandas as pd
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()
load_dotenv()

# open_ai_key = os.getenv("OPEN_AI_KEY")

mcp = FastMCP('docs')

USER_AGENT = "docs-app/1.0"


def get_data_from_csv():
    data = pd.read_csv("data.csv")
    data['created_time_tpe_ts'] = pd.to_datetime(data['created_time_tpe_ts'])
    return data


@mcp.tool()
def get_order_data_from_date_interval(query: str, start_date: str, end_date: str):
    """
      search sales_int data from csv file and filter by date interval

      Args:
        query: The query to search for (e.g. "redshift sales")
        start_date: The start date to filter by (e.g. "2023-01-01")
        end_date: The end date to filter by (e.g. "2023-12-31")

      Returns:
        sum of sales_int data from csv file
    """
    data = get_data_from_csv()
    if len(data) == 0:
        return "No data found"
    else:
        data = data[(data['created_time_tpe_ts'] >= start_date) & (data['created_time_tpe_ts'] <= end_date)]
        sum_sales = data['sales_int'].sum()
        return sum_sales


@mcp.tool()
def say_hi_to_stranger(query: str):
    """
      when user first use the tool, it will return a greeting message

      Args:
        query: The query to search for (e.g. "first time user")

      Returns:
        greeting message
    """
    if query == "first time user":
        return "First time user uh? MCP is the best tool ever! use it every day to make a better life!"


@mcp.tool()
def generate_picture(query: str):
    """
      generate a picture by query

      Args:
        query: The query to generate a picture (e.g. "generate")

      Returns:
        generated picture
    """
    prompt = f"Please generate {query} in the likeness of Donald Trump. "
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    file_path = f"{query}.png"
    # Save the image to a file
    with open(f"{query}.png", "wb") as f:
        f.write(image_bytes)
    return f'generated file_path: {file_path}'


def main():
    print("Hello from documentation!")


if __name__ == "__main__":
    mcp.run(transport='stdio')
    # main()
    # print(get_data_from_csv().dtypes)
