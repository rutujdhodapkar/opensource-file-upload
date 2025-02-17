def rail_fence_cipher_encrypt(text, key):
    rail = [['\n' for i in range(len(text))] for j in range(key)]
     
    dir_down = False
    row, col = 0, 0
     
    for i in range(len(text)):
        if row == 0 or row == key - 1:
            dir_down = not dir_down
         
        rail[row][col] = text[i]
        col += 1
         
        if dir_down:
            row += 1
        else:
            row -= 1
     
    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return "".join(result)
 
def rail_fence_cipher_decrypt(cipher, key):
    rail = [['\n' for i in range(len(cipher))] for j in range(key)]
     
    dir_down = None
    row, col = 0, 0
     
    for i in range(len(cipher)):
        if row == 0 or row == key - 1:
            dir_down = not dir_down
        rail[row][col] = '*'
        col += 1
         
        if dir_down:
            row += 1
        else:
            row -= 1
             
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1
         
    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0 or row == key - 1:
            dir_down = not dir_down
             
        if rail[row][col] != '*':
            result.append(rail[row][col])
            col += 1
             
        if dir_down:
            row += 1
        else:
            row -= 1
    return "".join(result)

def get_rail_matrix(text, key):
    # Build the zigzag rail matrix for the given text using empty strings as placeholders.
    matrix = [['' for _ in range(len(text))] for _ in range(key)]
    dir_down = False
    row, col = 0, 0
    for ch in text:
        if row == 0 or row == key - 1:
            dir_down = not dir_down
        matrix[row][col] = ch
        col += 1
        if dir_down:
            row += 1
        else:
            row -= 1
    return matrix

def print_in_tabular_format(data):
    # Determine the maximum width for each column for a neat display
    num_cols = len(data[0])
    col_widths = [max(len(str(row[i])) for row in data) for i in range(num_cols)]
    
    # Print header row
    header = data[0]
    print(" | ".join(header[i].ljust(col_widths[i]) for i in range(num_cols)))
    print("-+-".join('-' * col_widths[i] for i in range(num_cols)))
    
    # Print the remaining rows
    for row in data[1:]:
        print(" | ".join(row[i].ljust(col_widths[i]) for i in range(num_cols)))

def write_to_excel(data, filename):
    # Write data to a CSV file without using any external packages
    with open(filename, 'w', encoding='utf-8') as f:
        for row in data:
            f.write(','.join(str(item) for item in row) + '\n')

def main():
    choice = input("Enter 'e' to encrypt or 'd' to decrypt: ").lower()
    text = input("Enter the text: ")
    key = int(input("Enter the key: "))

    if choice == 'e':
        encrypted_text = rail_fence_cipher_encrypt(text, key)
        # For display, generate the rail matrix using the original plain text.
        rail_matrix = get_rail_matrix(text, key)
        # Create a header row with column numbers.
        header = [""] + [str(i + 1) for i in range(len(text))]
        table_data = [header]
        for idx, row in enumerate(rail_matrix):
            table_data.append(["Rail " + str(idx + 1)] + row)
        print_in_tabular_format(table_data)
        write_to_excel(table_data, r"C:\Users\STUDENT\Desktop\New Microsoft Excel Worksheet (2).xlsx")
        print("Excel file 'C:\\Users\\STUDENT\\Desktop\\New Microsoft Excel Worksheet (2).xlsx' has been created.")
    elif choice == 'd':
        decrypted_text = rail_fence_cipher_decrypt(text, key)
        # Generate the rail matrix from the decrypted text.
        rail_matrix = get_rail_matrix(decrypted_text, key)
        header = [""] + [str(i + 1) for i in range(len(decrypted_text))]
        table_data = [header]
        for idx, row in enumerate(rail_matrix):
            table_data.append(["Rail " + str(idx + 1)] + row)
        print_in_tabular_format(table_data)
        write_to_excel(table_data, r"C:\Users\STUDENT\Desktop\New Microsoft Excel Worksheet (2).xlsx")
        print("Excel file 'C:\\Users\\STUDENT\\Desktop\\New Microsoft Excel Worksheet (2).xlsx' has been created.")
    else:
        print("Invalid choice. Please enter 'e' or 'd'.")

if __name__ == "__main__":
    main()
