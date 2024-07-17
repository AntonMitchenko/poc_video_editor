# Guide to Using Replicate's Python Client

This guide will help you get started with using Replicate's Python client library to interact with their API and run models.

## Installation

First, you need to install Replicate’s Python client library. You can do this using pip:

```bash
pip install replicate
```

## Setting Up

After installing the library, you need to set the `REPLICATE_API_TOKEN` environment variable. This token can be found in your account settings on the Replicate website.

```bash
export REPLICATE_API_TOKEN=<paste-your-token-here>
```

Replace `<paste-your-token-here>` with your actual API token.

## Usage

### Importing the Client

To start using the library, you need to import the client in your Python script:

```python
import replicate
```

### Running a Model

You can run models using Replicate’s API. Here is an example of how to run the `riffusion/riffusion` model. Check out the model's API reference for a detailed overview of the input/output schemas.

```python
output = replicate.run(
    "riffusion/riffusion:8cf61ea6c56afd61d8f5b9ffd14d7c216c0a93844ce2d82ac1c9ecc9c7f24e05",
    input={
        "alpha": 0.5,
        "prompt_a": "funky synth solo",
        "prompt_b": "90's rap",
        "denoising": 0.75,
        "seed_image_id": "vibes",
        "num_inference_steps": 50
    }
)
print(output)
```

### Further Reading

To learn more, take a look at the [guide on getting started with Python](https://replicate.com/docs/getting-started/python).

By following this guide, you should be able to set up and use Replicate's Python client to run models and interact with their API effectively.