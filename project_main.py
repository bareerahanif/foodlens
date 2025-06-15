from image import Image
from model_factory import ModelFactory
from authentication import AuthenticationManager
import os

def authenticate_user(auth_manager):
    while True:
        print("\n1. Login")
        print("2. Sign Up")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            email = input("Email: ")
            password = input("Password: ")
            success, message, session_id = auth_manager.login(email, password)
            print(message)
            if success:
                return email
        elif choice == "2":
            username = input("Username: ")
            email = input("Email: ")
            password = input("Password: ")
            dob = input("Date of Birth (YYYY-MM-DD): ")
            success, message = auth_manager.sign_up(username, email, password, dob)
            print(message)
            if success:
                continue
        elif choice == "3":
            return None
        else:
            print("Invalid choice")

def get_image_path():
    while True:
        print("\nPlease enter the path to your food image")
        print("Example: /home/user/Pictures/food.jpg or C:\\Users\\user\\Pictures\\food.jpg")
        image_path = input("Image path: ").strip()
        
        if not os.path.exists(image_path):
            print("Error: File does not exist. Please try again.")
            continue
            
        if os.path.isdir(image_path):
            print("Error: You entered a directory. Please enter the full path to an image file.")
            continue
            
        if not image_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            print("Error: Only JPG/JPEG/PNG images are supported.")
            continue
            
        return image_path

def analyze_image(tier, image_path):
    try:
        image_id = os.path.basename(image_path).split('.')[0]
        
        size_mb = os.path.getsize(image_path) / (1024 * 1024)
        
        img_format = image_path.split('.')[-1].lower()
        
        img = Image(
            imageID=image_id,  
            filePath=image_path,
            format=img_format,
            size=size_mb,
            resolution="N/A"
        )
        
        if not img.validateImageFormat():
            print("Error: Invalid image format. Please use JPG, JPEG, or PNG.")
            return False
            
        if not img.validateImageSize():
            print(f"Error: Image size ({size_mb:.2f} MB) exceeds 5MB limit.")
            return False
            
        if not img.uploadImage():
            print("Error: Failed to process image.")
            return False
            
        detector = ModelFactory.get_model(tier)
        results = detector.analyze(img)
        
        print(f"\n[RESULTS] Using {tier.title()} tier")
        for result in results:
            if 'message' in result:
                print(f"{result['name'].title()} - {result['message']}")
            else:
                print(f"{result['name'].title()} - {result['calories']} kcal")
        
        corporate_items = [r for r in results if 'message' in r and 'corporate' in r['message'].lower()]
        if corporate_items and tier == "personal":
            print("\n[UPGRADE] Some items require Corporate tier for full analysis.")
            
        return True
        
    except Exception as e:
        print(f"Error analyzing image: {str(e)}")
        return False

def main():
    auth_manager = AuthenticationManager()
    print("Welcome to FoodLens!")
    
    user_email = authenticate_user(auth_manager)
    if not user_email:
        print("Goodbye!")
        return
    
    user_info = auth_manager.get_user_info(user_email)
    tier = user_info.get('tier', 'personal')
    
    while True:
        print(f"\nLogged in as: {user_info['username']} ({tier} tier)")
        print("\nMain Menu:")
        print("1. Analyze food image")
        print("2. Change subscription tier")
        print("3. Logout")
        
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            image_path = get_image_path()
            analyze_image(tier, image_path)
        elif choice == "2":
            print("\nSelect tier:")
            print("1. Personal (Basic)")
            print("2. Corporate (Advanced)")
            tier_choice = input("Enter choice: ").strip()
            if tier_choice == "2":
                tier = "corporate"
                print("Tier changed to Corporate (demo mode)")
            else:
                tier = "personal"
                print("Tier changed to Personal")
        elif choice == "3":
            auth_manager.logout(user_email)
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()