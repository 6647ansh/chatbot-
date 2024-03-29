{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "source": [
        "url = \"https://ispo.ucsd.edu/\""
      ],
      "metadata": {
        "id": "SibWAaBRzQC7"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "%%capture\n",
        "!apt-get update"
      ],
      "metadata": {
        "id": "xd-GipqDOk5L"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "import os\n",
        "import jsonlines\n",
        "import json\n",
        "import openai\n",
        "from webpage_scraper import extract_data_from_website\n",
        "from tqdm import tqdm\n",
        "from selenium import webdriver\n",
        "from selenium.webdriver import FirefoxOptions\n",
        "from selenium.webdriver.common.by import By\n",
        "from selenium.webdriver.support.ui import WebDriverWait\n",
        "from selenium.webdriver.support import expected_conditions as EC\n",
        "opts = FirefoxOptions()\n",
        "opts.add_argument(\"--headless\")\n"
      ],
      "metadata": {
        "id": "jce-sHCvR691"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "driver = webdriver.Firefox(options=opts)\n",
        "\n",
        "def visit_links(url, visited = set()):\n",
        "    TAG_NAME = \"a\"\n",
        "    if url not in visited and 'ispo' in url:\n",
        "        try:\n",
        "            driver.get(url)\n",
        "            visited.add(url)\n",
        "            print(f\"Visited {url}\")\n",
        "            links = driver.find_elements(By.TAG_NAME, 'a')\n",
        "            for link in links:\n",
        "                href = link.get_attribute('href')\n",
        "                if href and 'ispo' in href:\n",
        "                    visited = visit_links(href, visited)\n",
        "        except Exception as e:\n",
        "            print(f\"Error visiting {url}: {e}\")\n",
        "    return visited\n",
        "\n",
        "url = \"https://ispo.ucsd.edu/\"\n",
        "visited_links = visit_links(url)\n",
        "\n",
        "driver.quit()\n"
      ],
      "metadata": {
        "id": "XtzSq6Dl27kV"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def get_website_text(visited_links):\n",
        "  final_data = []\n",
        "  for url in visited_links:\n",
        "      f = open(f\"/content/{url[8:].replace('/', '_')}.txt\", \"w\")\n",
        "      try:\n",
        "          data = extract_data_from_website(url)\n",
        "          final_data.append(data)\n",
        "          f.write(data)\n",
        "          f.close()\n",
        "      except:\n",
        "          os.remove(f\"/content/{url[8:].replace('/', '_')}.txt\")\n",
        "          print(f\"{url} empty\")\n",
        "  return final_data\n",
        "\n",
        "final_data = get_website_text(visited_links)"
      ],
      "metadata": {
        "id": "VcizDmSo-7Lk"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def count_statistics(passages):\n",
        "    total_characters = 0\n",
        "    total_words = 0\n",
        "    total_sentences = 0\n",
        "\n",
        "    for passage in passages:\n",
        "        # Counting characters\n",
        "        total_characters += len(passage)\n",
        "\n",
        "        # Counting words\n",
        "        words = passage.split()\n",
        "        total_words += len(words)\n",
        "\n",
        "        # Counting sentences\n",
        "        sentences = passage.split('.')\n",
        "        total_sentences += len(sentences)\n",
        "\n",
        "    return total_characters, total_words, total_sentences\n",
        "\n",
        "count_statistics(final_data)"
      ],
      "metadata": {
        "id": "TI2jtGAUbdwj"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def split_string(string, length):\n",
        "    lines = []\n",
        "    current_chunk = \"\"\n",
        "\n",
        "    for line in string.split(\"\\n\"):\n",
        "        if len(current_chunk) + len(line) <= length:\n",
        "            current_chunk += line + \"\\n\"\n",
        "        else:\n",
        "            lines.append(current_chunk)\n",
        "            current_chunk = line + \"\\n\"\n",
        "\n",
        "    # Add the last remaining chunk, if any\n",
        "    if current_chunk:\n",
        "        lines.append(current_chunk)\n",
        "\n",
        "    return lines\n"
      ],
      "metadata": {
        "id": "Dw66uqw5Iig0"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def website_chunked(final_text_data):\n",
        "  input_data = []\n",
        "  for page in final_text_data:\n",
        "    if (len(page)) < 2000:\n",
        "      input_data.append(page)\n",
        "    else:\n",
        "      input_data.extend(split_string(page, 2000-1))\n",
        "  return input_data"
      ],
      "metadata": {
        "id": "owIIQ3eu1P6A"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "os.environ[\"OPENAI_API_KEY\"] = \"<insert API token>\"\n",
        "\n",
        "def get_web_data_chunked(url):\n",
        "  jsonl_file = \"/content/finetuning_data_websites_chatgpt.jsonl\"\n",
        "  visited_urls = visit_links(url)\n",
        "  print(len(visited_urls))\n",
        "  final_text_data = get_website_text(visited_links)\n",
        "  print(len(final_text_data))\n",
        "  website_chunked_data = website_chunked(final_text_data)\n",
        "  print(len(website_chunked_data))\n",
        "  print(count_statistics(website_chunked_data))\n",
        "  num_requests = 0\n",
        "  t = website_chunked_data\n",
        "  with jsonlines.open(jsonl_file, mode='a') as writer:\n",
        "      for text in tqdm(t, desc=\"Processing Texts\"):\n",
        "          completion = openai.ChatCompletion.create(\n",
        "              model=\"gpt-3.5-turbo\",\n",
        "              temperature=0.1,\n",
        "              max_tokens=2000,\n",
        "              messages=[\n",
        "                  {\"role\": \"system\", \"content\": \"You are a language expert who needs to help create Question Answer pairs from a given piece of text.\"},\n",
        "                  {\"role\": \"user\", \"content\": f'Text: \\n{text}\\n\\nTask: Generate up to 10 logical prompt completion pairs from this text. The output should not be numbered and strictly use the following format for your response ' + '{\"prompt\": <text for prompt>, \"completion\": <text for completion>}'}\n",
        "              ]\n",
        "          )\n",
        "          num_requests += 1\n",
        "          sample = completion.choices[0].message.content\n",
        "\n",
        "          split_samples = [i for i in sample.split('\\n') if len(i) != 0 and \"prompt\" in i and \"completion\" in i]\n",
        "          for pair in split_samples:\n",
        "              start_index = pair.find(\"{\")\n",
        "              end_index = pair.rfind(\"}\")\n",
        "              if start_index != -1 and end_index != -1:\n",
        "                pair = pair[start_index:end_index+1]\n",
        "\n",
        "              p = json.loads(pair)\n",
        "              p['prompt'] = p['prompt'] + \"\\n\\n###\\n\\n\"\n",
        "              p['completion'] = p['completion'] + \"###\"\n",
        "              writer.write(p)\n",
        "get_web_data_chunked(url)"
      ],
      "metadata": {
        "id": "tO_GokdhKi-h"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}
