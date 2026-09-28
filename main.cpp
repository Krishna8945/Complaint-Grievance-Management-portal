#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main(int argc, char* argv[]) {
    // Expected arguments: main.exe "Title" "Category" "Description" "Status" "ImageName"
    if (argc < 4) {
        cout << "Error: Missing required arguments" << endl;
        return 1;
    }

    string title = argv[1];
    string category = argv[2];
    string description = argv[3];
    string status = (argc >= 5) ? argv[4] : "Pending";
    string image = (argc >= 6) ? argv[5] : "";

    // Save to complaints.txt in Append Mode
    ofstream file("complaints.txt", ios::app);
    if (file.is_open()) {
        file << title << " | " << category << " | " << description << " | " << status << " | " << image << endl;
        file.close();
        cout << "Success" << endl;
    } else {
        cout << "Error: Unable to open file" << endl;
        return 1;
    }

    return 0;
}