import os
# Matplotlib kütüphanesini içeri alıyoruz
# Genelde 'plt' kısaltmasıyla kullanılır
import matplotlib as plt

filename = "my_books.txt"

# --- FILE OPERATIONS ---

def check_if_file_exists():
    if os.path.exists(filename):
        return True
    else:
        return False

def get_all_books():
    book_list = []
    file_exists = check_if_file_exists()
    
    if file_exists == True:
        f = open(filename, "r")
        all_lines = f.readlines()
        f.close()
        
        for line in all_lines:
            clean_line = line.strip()
            parts = clean_line.split(",")
            
            if len(parts) == 2:
                book_name = parts[0]
                rating_str = parts[1]
                
                if rating_str.isdigit():
                    book = {"title": book_name, "rating": int(rating_str)}
                    book_list.append(book)
    return book_list

def save_book_to_file(name, rating):
    f = open(filename, "a")
    line = name + "," + str(rating) + "\n"
    f.write(line)
    f.close()
    print("Success: Book saved.")

# --- ERROR HANDLING ---

def check_duplicate_book(new_name):
    current_books = get_all_books()
    for book in current_books:
        # İsimleri küçük harfe çevirip kontrol et
        if book["title"].lower() == new_name.lower():
            return True 
    return False

# --- NEW: MATPLOTLIB VISUALISATION ---

def show_graph_statistics(books):
    if len(books) == 0:
        print("No data to plot.")
        return

    print("Generating graph... Please check the new window.")

    # Grafik için iki listeye ihtiyacımız var: X ve Y ekseni
    # X ekseni: Puanlar (1'den 10'a kadar)
    # Y ekseni: O puana sahip kaç kitap var?
    
    x_scores = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y_counts = []

    for score in x_scores:
        count = 0
        for book in books:
            if book["rating"] == score:
                count = count + 1
        y_counts.append(count)

    # Basit bir Sütun Grafiği (Bar Chart) çiziyoruz
    plt.figure(figsize=(8, 5)) # Pencere boyutu
    plt.bar(x_scores, y_counts, color='skyblue')
    
    # Başlık ve etiketler (Hoca bunları sever)
    plt.title('My Book Ratings Distribution')
    plt.xlabel('Rating (1-10)')
    plt.ylabel('Number of Books')
    
    # X ekseninde sadece 1-10 sayıları görünsün
    plt.xticks(x_scores)
    
    # Izgara çizgileri ekle ki okunması kolay olsun
    plt.grid(axis='y', linestyle='--')
    
    # Grafiği göster
    plt.show()

# --- MENUS AND SORTING ---

def add_book_menu():
    print("\n--- Add New Book ---")
    name = input("Enter Book Title: ")
    
    if len(name) > 0:
        is_duplicate = check_duplicate_book(name)
        
        if is_duplicate == False:
            rating_input = input("Enter Rating (1-10): ")
            
            if rating_input.isdigit():
                rating = int(rating_input)
                if rating >= 1 and rating <= 10:
                    save_book_to_file(name, rating)
                else:
                    print("Error: Rating must be 1-10.")
            else:
                print("Error: Please enter a number.")
        else:
            print("Error: Book already exists.")
    else:
        print("Error: Name cannot be empty.")

def sort_books(books):
    # Bubble Sort
    n = len(books)
    for i in range(n):
        for j in range(0, n - i - 1):
            if books[j]["rating"] < books[j + 1]["rating"]:
                temp = books[j]
                books[j] = books[j + 1]
                books[j + 1] = temp
    return books

def show_list_menu():
    books = get_all_books()
    if len(books) == 0:
        print("Library is empty.")
    else:
        sorted_books = sort_books(books)
        print("\n--- MY BOOKS (Sorted) ---")
        for b in sorted_books:
            print(f"{b['title']:<20} -> {b['rating']}/10")

def main():
    running = True
    print("=== My Smart Library (with Visuals) ===")
    
    while running == True:
        print("\nMENU")
        print("1. Add Book")
        print("2. List Books (Sorted)")
        print("3. View Graph (Matplotlib)")
        print("4. Exit")
        
        sel = input("Choice: ")
        
        if sel == "1":
            add_book_menu()
        elif sel == "2":
            show_list_menu()
        elif sel == "3":
            data = get_all_books()
            # Matplotlib fonksiyonunu çağırıyoruz
            show_graph_statistics(data)
        elif sel == "4":
            print("Bye!")
            running = False
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()