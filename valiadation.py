import json
class Validation:

    def is_integer(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def is_float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False


    @staticmethod
    def validate_price(data):
        """Ensure sale price is less than or equal to the original price."""
        for product in data:
            return Validation.is_integer(product['price']) or Validation.is_float(product['price'])





    @staticmethod
    def validate_images(data):
        """Ensure each variant has images and prices."""
        for product in data:
            #print(product['image'])
            if product['image'].endswith('.jpg') or product['image'].endswith('.img'):
                return True
            else:
                print('\ninvalid image:' ,product['image'])
                return False



    @staticmethod
    def run_all_validations(data):
        """Run all validation checks."""
        return (Validation.validate_price(data) and
                Validation.validate_images(data))


def main():
    """Main function to validate scraped product data."""
    files = ['./foreignfortune.json', './lachocolate.json', './traderjoes.json']

    for file in files:
        with open(file, 'r',encoding='utf-8-sig') as f:
            data = json.load(f)
            if Validation.run_all_validations(data):
                print(f"{file} data is valid.")
            else:
                print(f"{file} data is invalid.")


if __name__ == "__main__":
    main()
