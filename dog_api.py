"""
Assignment Overview:

You are building a Dog Image Browser using the Dog CEO REST API.

The app should allow users to:
- View a list of all available dog breeds
- Get a random image of a breed
- Get a random image from a sub-breed

You will be using the Dog CEO API: https://dog.ceo/dog-api/

Your app should display a main menu with the following options:
1. Show all breeds
2. Get a random image from a breed
3. Get a random image from a sub-breed
4. Exit

The system should handle the following errors:
- Handling errors when a user enters an invalid menu option
- Handling errors when a user enters a breed that does not exist
- Handling errors when a user enters a sub-breed that does not exist
- Handling connection errors when calling the API

If there is an error you should print your own custom error message to the user and allow them to try again.
- Hint: you can use a while loop + try / except blocks to handle this

You should use try / except blocks to handle these errors.

You can either use the should use the requests library or the http.client library to make your requests
"""

import requests

def get_all_breeds():
    """GET request to fetch all dog breeds."""
    try:
        response = requests.get("https://dog.ceo/api/breeds/list/all")
        response.raise_for_status()
        data = response.json()
        return data["message"]
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not fetch breed list from API. Details: {e}")
        return {}

def get_random_image(breed):
    """
    GET request to fetch a random image from a breed.
   
    Args:
        breed (str): The name of the dog breed
       
    Returns:
        str: URL of a random dog image or error message
    """
    try:
        url = f"https://dog.ceo/api/breed/{breed}/images/random"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
       
        if data["status"] == "success":
            return data["message"]
        else:
            return None
           
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return None
        else:
            return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.RequestException:
        return None
    except Exception:
        return None

def get_random_sub_breed_image(breed, sub_breed):
    """
    GET request to fetch a random image from a sub-breed.
   
    Args:
        breed (str): The name of the dog breed
        sub_breed (str): The name of the dog sub-breed
       
    Returns:
        str: URL of a random dog image or None if error
    """
    try:
        url = f"https://dog.ceo/api/breed/{breed}/{sub_breed}/images/random"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
       
        if data["status"] == "success":
            return data["message"]
        else:
            return None
           
    except requests.exceptions.HTTPError:
        return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.RequestException:
        return None
    except Exception:
        return None

def show_breeds():
    """Fetches all breeds and prints them sorted, 5 per line."""
    breeds_dict = get_all_breeds()
   
    if not breeds_dict:
        print("No breeds available to display.")
        return
   
    print("\nAvailable Dog Breeds:")
    print("---------------------")
   
    # Get sorted list of breeds
    breeds_list = sorted(breeds_dict.keys())
   
    # Display breeds 5 per line
    for i in range(0, len(breeds_list), 5):
        # Get next 5 breeds (or fewer if at the end)
        line_breeds = breeds_list[i:i+5]
        # Print them on one line with proper spacing
        print("  ".join(line_breeds))
   
    print(f"\nTotal: {len(breeds_list)} breeds")

def main():
    print("Welcome to the Dog Image Browser!")
   
    while True:
        print("\nWhat would you like to do?")
        print("1. Show all breeds")
        print("2. Get a random image from a breed")
        print("3. Get a random image from a sub-breed")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            show_breeds()

        elif choice == "2":
            breeds = get_all_breeds()
            if not breeds:
                print("Unable to fetch breeds. Please try again later.")
                continue
               
            # Display available breeds
            print("\nAvailable breeds:")
            show_breeds(breeds)
           
            # Get breed from user
            breed = input("\nEnter breed name: ").strip().lower()
           
            # Check if breed exists
            if breed not in breeds:
                print(f"Error: '{breed}' is not a valid breed.")
                continue
           
            # Get random image
            image_url = get_random_image(breed)
           
            # Check if it's an error message or a URL
            if image_url.startswith("http"):
                print(f"\nRandom image URL for {breed}: {image_url}")
            else:
                print(image_url)  # Print error message

        elif choice == "3":
            breeds = get_all_breeds()
            if not breeds:
                print("Unable to fetch breeds. Please try again later.")
                continue
               
            # Display available breeds
            print("\nAvailable breeds:")
            show_breeds(breeds)
           
            # Get breed from user
            breed = input("\nEnter breed name: ").strip().lower()
           
            # Check if breed exists
            if breed not in breeds:
                print(f"Error: '{breed}' is not a valid breed.")
                continue
           
            # Check if the breed has sub-breeds
            sub_breeds = breeds[breed]
            if not sub_breeds:
                print(f"Error: The '{breed}' breed does not have any sub-breeds.")
                continue
           
            # Display available sub-breeds
            print(f"\nAvailable sub-breeds for {breed}:")
            for i, sub_breed in enumerate(sorted(sub_breeds), 1):
                print(f"{i}. {sub_breed}")
           
            # Get sub-breed from user
            sub_breed = input("\nEnter sub-breed name: ").strip().lower()
           
            # Check if sub-breed exists
            if sub_breed not in sub_breeds:
                print(f"Error: '{sub_breed}' is not a valid sub-breed of '{breed}'.")
                continue
           
            # Get random image
            image_url = get_random_sub_breed_image(breed, sub_breed)
           
            # Check if it's an error message or a URL
            if image_url.startswith("http"):
                print(f"\nRandom image URL for {breed} {sub_breed}: {image_url}")
            else:
                print(image_url)  # Print error message

        elif choice == "4":
            print("Thank you for using the Dog Image Browser. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a number between 1 and 4.")

if __name__ == "__main__":
    main()