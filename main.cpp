#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main(int argc, char* argv[]) {
    // Arguments: main title category description [status]
    if (argc < 4) {
        cout << "Error: Invalid Arguments" << endl;
        return 1;
    }

    string title = argv[1];
    string category = argv[2];
    string description = argv[3];
    string status = (argc >= 5) ? argv[4] : "Pending";

    // Open file in append mode
    ofstream file("complaints.txt", ios::app);
    if (file.is_open()) {
        file << title << " | " << category << " | " << description << " | " << status << endl;
        file.close();
        cout << "Success" << endl;
    } else {
        cout << "Error: Unable to open file" << endl;
        return 1;
    }

    return 0;
}