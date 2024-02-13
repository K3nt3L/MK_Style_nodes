from abc import ABC, abstractmethod
import json
import os
import random
import time

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding="utf8", errors='ignore') as file:
            json_data = json.load(file)
            return json_data
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def read_sdxl_styles(json_data):
    if not isinstance(json_data, list):
        print("Error: input data must be a list")
        return None

    names = []

    for item in json_data:
        if isinstance(item, dict):
            if 'name' in item:
                names.append(item['name'])

    return names

def read_sdxl_templates_replace_and_combine(json_data, template_name, positive_prompt, negative_prompt):
    try:
        if not isinstance(json_data, list):
            raise ValueError("Invalid JSON data. Expected a list of templates.")

        for template in json_data:
            if 'name' not in template or 'prompt' not in template:
                continue  # Skip templates that are missing 'name' or 'prompt' fields

            if template['name'] == template_name:
                positive_prompt = template['prompt'].replace('{prompt}', positive_prompt)

                json_negative_prompt = template.get('negative_prompt', "")
                if negative_prompt:
                    negative_prompt = f"{json_negative_prompt}, {negative_prompt}" if json_negative_prompt else negative_prompt
                else:
                    negative_prompt = json_negative_prompt

                return positive_prompt, negative_prompt

        raise ValueError(f"No template found with name '{template_name}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# MISC
class SDXLPromptStylerMisc:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_misc.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'MK Style Prompts'
    # Nom catégorie noueds dans menu contextuel

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# NODE ALL
class SDXLPromptStylerAll:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        p = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(p, 'sdxl_styles_all.json')
        cls.json_data = read_json_file(file_path)
        styles = read_sdxl_styles(cls.json_data)

        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
            "optional": {
                "auto_select_style": ("BOOLEAN", {"default": False}),
                "auto_refresh": ("BOOLEAN", {"default": False}),
            }
        }
    
    @classmethod
    def IS_CHANGED(cls, text, autorefresh):
        # Force re-evaluation of the node
        if auto_refresh == "True":
            return float("NaN")

    def get_prompt(self, text: str, autorefresh: str) -> tuple[str]:
        prompt = self.generate_prompt(text)
        print(f"Prompt: {prompt}")

        return (prompt,)

    @abstractmethod
    def generate_prompt(self, text: str) -> str:
        ...

    
    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt, auto_select_style=False, auto_refresh=False):
        if auto_select_style or auto_refresh:
            style = random.choice([template['name'] for template in self.json_data])

        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)

        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        # Introduce a timestamp-based change using the current time
        current_time = int(time.time())
        dummy_change = current_time

        return positive_prompt, negative_prompt, dummy_change
        dummy_change = current_time

        return positive_prompt, negative_prompt, dummy_change   # Include dummy_change to trigger execution
        
# HORROR
class SDXLPromptStylerHorror:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_horror.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# BY ARTIST
class SDXLPromptStylerbyArtist:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_artists.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# FOCUS
class SDXLPromptStylerbyFocus:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_focus.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# THEME
class SDXLPromptStylerbyTheme:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_themes.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# Environment
class SDXLPromptStylerbyEnvironment:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_environment.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# MOOD
class SDXLPromptStylerbyMood:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_mood.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# SUBJECT
class SDXLPromptStylerbySubject:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_subject.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# TIMEofDAY
class SDXLPromptStylerbyTimeofDay:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_tod.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# CAMERA
class SDXLPromptStylerbyCamera:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_camera.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# COMPOSITION
class SDXLPromptStylerbyComposition:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_composition.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# LIGHTING
class SDXLPromptStylerbyLighting:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_lighting.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# DEPTH
class SDXLPromptStylerbyDepth:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_depth.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# FILTER
class SDXLPromptStylerbyFilter:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_filter.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# ORIGINAL
class SDXLPromptStylerbyOriginal:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_original.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# MileHigh
class SDXLPromptStylerbyMileHigh:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_mh.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt
        
# FANTASY
class SDXLPromptStylerbyFantasySetting:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_fs.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# Mythical Creatures
class SDXLPromptStylerbyMythicalCreature:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_mc.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# Surrealism
class SDXLPromptStylerbySurrealism:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_surrealism.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# Impressionism
class SDXLPromptStylerbyImpressionism:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_impressionism.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# CyberPunk Surrealism
class SDXLPromptStylerbyCyberpunkSurrealism:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_cs.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# Quantum Surrealism
class SDXLPromptStylerbyQuantumRealism:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_qr.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# SteamPunk Realism
class SDXLPromptStylerbySteamPunkRealism:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_sr.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# Wyvern
class SDXLPromptStylerbyWyvern:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_wyvern.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# DOUBLON ?
class SDXLPromptStylerbyWyvern:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_wyvern.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# Gothic Revival
class SDXLPromptbyGothicRevival:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_gothrev.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# Celtic ART
class SDXLPromptbyCelticArt:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_celticart.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# Irisih folk art
class SDXLPromptbyIrishFolkArt:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_irishfolkart.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# SportART
class SDXLPromptbySportsArt:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_sports.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# Fashion Art
class SDXLPromptbyFashionArt:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_fashion.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# WildLife ART
class SDXLPromptbyWildlifeArt:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_wildlife.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# Street Art
class SDXLPromptbyStreetArt:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_street.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# VikingArt
class SDXLPromptbyVikingArt:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_viking.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# romantic nationalism
class SDXLPromptbyRomanticNationalismArt:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_romanticnat.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# ContemporaryNordicAr
class SDXLPromptbyContemporaryNordicArt:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        # Get current file's directory
        p = os.path.dirname(os.path.realpath(__file__))
        # Construct 'sdxl_styles.json' path
        file_path = os.path.join(p, 'sdxl_styles_contempnordic.json')

        # Read JSON from file
        self.json_data = read_json_file(file_path)
        # Retrieve styles from JSON data
        styles = read_sdxl_styles(self.json_data)
        
        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
        }

    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt):
        # Process and combine prompts in templates
        # The function replaces the positive prompt placeholder in the template,
        # and combines the negative prompt with the template's negative prompt, if they exist.
        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)
 
        # If logging is enabled (log_prompt is set to "Yes"), 
        # print the style, positive and negative text, and positive and negative prompts to the console
        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt

# IcelandicContemporaryArt
class SDXLPromptbyIcelandicContemporaryArt:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        p = os.path.dirname(os.path.realpath(__file))
        file_path = os.path.join(p, 'sdxl_styles_all.json')
        self.json_data = read_json_file(file_path)
        styles = read_sdxl_styles(self.json_data)

        return {
            "required": {
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
                "style": ((styles), ),
                "log_prompt": (["No", "Yes"], {"default":"No"}),
            },
            "optional": {
                "random_style": ("BOOLEAN", {"default": False}),  # Add a boolean parameter for random style selection
            }
        }
    
    RETURN_TYPES = ('STRING','STRING',)
    RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g',)
    FUNCTION = 'prompt_styler'
    CATEGORY = 'Style Prompts'

    def prompt_styler(self, text_positive, text_negative, style, log_prompt, random_style=False):
        if random_style:
            style = random.choice([template['name'] for template in self.json_data])
        else:
            style = text_positive  # You can change this to the appropriate parameter

        positive_prompt, negative_prompt = read_sdxl_templates_replace_and_combine(self.json_data, style, text_positive, text_negative)

        if log_prompt == "Yes":
            print(f"style: {style}")
            print(f"text_positive: {text_positive}")
            print(f"text_negative: {text_negative}")
            print(f"positive_prompt: {positive_prompt}")
            print(f"negative_prompt: {negative_prompt}")

        return positive_prompt, negative_prompt, style

# NOMMMER LES NOEUDS

NODE_CLASS_MAPPINGS = {
    "SDXLPromptStylerAll": SDXLPromptStylerAll,
    "SDXLPromptStylerbyArtist": SDXLPromptStylerbyArtist,
    "SDXLPromptStylerbyCamera": SDXLPromptStylerbyCamera,
    "SDXLPromptbyCelticArt": SDXLPromptbyCelticArt,
    "SDXLPromptStylerbyComposition": SDXLPromptStylerbyComposition,    
    "SDXLPromptbyContemporaryNordicArt": SDXLPromptbyContemporaryNordicArt,
    "SDXLPromptStylerbyCyberpunkSurrealism": SDXLPromptStylerbyCyberpunkSurrealism,
    "SDXLPromptStylerbyDepth": SDXLPromptStylerbyDepth,
    "SDXLPromptStylerbyEnvironment": SDXLPromptStylerbyEnvironment,
    "SDXLPromptStylerbyFantasySetting": SDXLPromptStylerbyFantasySetting,    
    "SDXLPromptbyFashionArt": SDXLPromptbyFashionArt,    
    "SDXLPromptStylerbyFilter": SDXLPromptStylerbyFilter,
    "SDXLPromptStylerbyFocus": SDXLPromptStylerbyFocus,
    "SDXLPromptbyGothicRevival": SDXLPromptbyGothicRevival,
    "SDXLPromptStylerHorror": SDXLPromptStylerHorror,
    
    
    "SDXLPromptStylerbyImpressionism": SDXLPromptStylerbyImpressionism,
    "SDXLPromptbyIrishFolkArt": SDXLPromptbyIrishFolkArt,
    "SDXLPromptStylerbyLighting": SDXLPromptStylerbyLighting,
    "SDXLPromptStylerbyMileHigh": SDXLPromptStylerbyMileHigh,
    "SDXLPromptStylerMisc": SDXLPromptStylerMisc,
    "SDXLPromptStylerbyMood": SDXLPromptStylerbyMood,
    "SDXLPromptStylerbyMythicalCreature": SDXLPromptStylerbyMythicalCreature,    
    "SDXLPromptStylerbyOriginal": SDXLPromptStylerbyOriginal,
    "SDXLPromptStylerbyQuantumRealism": SDXLPromptStylerbyQuantumRealism,
    "SDXLPromptbyRomanticNationalismArt": SDXLPromptbyRomanticNationalismArt,
    "SDXLPromptbySportsArt": SDXLPromptbySportsArt,    
    "SDXLPromptStylerbySteamPunkRealism": SDXLPromptStylerbySteamPunkRealism,    
    "SDXLPromptbyStreetArt": SDXLPromptbyStreetArt,
    "SDXLPromptStylerbySubject": SDXLPromptStylerbySubject,
    "SDXLPromptStylerbySurrealism": SDXLPromptStylerbySurrealism,
    "SDXLPromptStylerbyTheme": SDXLPromptStylerbyTheme,
    "SDXLPromptStylerbyTimeofDay": SDXLPromptStylerbyTimeofDay,
    "SDXLPromptbyVikingArt": SDXLPromptbyVikingArt,
    "SDXLPromptbyWildlifeArt": SDXLPromptbyWildlifeArt,    
    "SDXLPromptStylerbyWyvern": SDXLPromptStylerbyWyvern,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SDXLPromptStylerAll": "Prompt Styler All",
    "SDXLPromptStylerbyArtist": "Prompt Styler Artist",
    "SDXLPromptStylerbyCamera": "Prompt Styler Camera",
    "SDXLPromptbyCelticArt": "Prompt Styler Celtic Art",
    "SDXLPromptStylerbyComposition": "Prompt Styler Composition",    
    "SDXLPromptbyContemporaryNordicArt": "Prompt Styler Contemporary Nordic Art",
    "SDXLPromptStylerbyCyberpunkSurrealism": "Prompt Styler Cyberpunk Surrealism",
    "SDXLPromptStylerbyDepth": "Prompt Styler Depth",
    "SDXLPromptStylerbyEnvironment": "Prompt Styler Environment",
    "SDXLPromptStylerbyFantasySetting": "Prompt Styler Fantasy-Setting",
    "SDXLPromptbyFashionArt": "Prompt Styler Fashion",
    "SDXLPromptStylerbyFilter": "Prompt Styler Filter",
    "SDXLPromptStylerbyFocus": "Prompt Styler Focus",
    "SDXLPromptbyGothicRevival": "Prompt Styler Gothic Revival",
    "SDXLPromptStylerHorror": "Prompt Styler Horror",
    
    
    "SDXLPromptStylerbyImpressionism": "Prompt Styler Impressionism",
    "SDXLPromptbyIrishFolkArt": "Prompt Styler Irish Folk Art",
    "SDXLPromptStylerbyLighting": "Prompt Styler Lighting",
    "SDXLPromptStylerbyMileHigh": "Prompt Styler MileHigh",
    "SDXLPromptStylerMisc": "Prompt Styler Misc",
    "SDXLPromptStylerbyMood": "Prompt Styler Mood",
    "SDXLPromptStylerbyMythicalCreature": "Prompt Styler Mythical Creature",    
    "SDXLPromptStylerbyOriginal": "Prompt Styler Original",
    "SDXLPromptStylerbyQuantumRealism": "Prompt Styler Quantum Realism",
    "SDXLPromptbyRomanticNationalismArt": "Prompt Styler Romantic Nationalism",
    "SDXLPromptbySportsArt": "Prompt Styler Sports",
    "SDXLPromptStylerbySteamPunkRealism": "Prompt Styler SteamPunk Realism",    
    "SDXLPromptbyStreetArt": "Prompt Styler Street",
    "SDXLPromptStylerbySubject": "Prompt Styler Subject",
    "SDXLPromptStylerbySurrealism": "Prompt Styler Surrealism",
    "SDXLPromptStylerbyTheme": "Prompt Styler Theme",
    "SDXLPromptStylerbyTimeofDay": "Prompt Styler Time of Day",    
    "SDXLPromptbyVikingArt": "Prompt Styler Viking Art",
    "SDXLPromptbyWildlifeArt": "Prompt Styler Wildlife",
    "SDXLPromptStylerbyWyvern": "Prompt Styler Wyvern",
}
