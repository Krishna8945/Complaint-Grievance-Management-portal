#include <iostream>
#include <fstream>
#include <string>

using namespace std;

class ComplaintManager {
public:
    void saveComplaint(const string& title, const string& category, const string& desc) {
        ofstream file("complaints.txt", ios::app);
        if (file.is_open()) {
            file << title << " | " << category << " | " << desc << "\n";
            file.close();
            cout << "SUCCESS";
        } else {
            cout << "ERROR";
        }
    }
};

int main(int argc, char* argv[]) {
    if (argc >= 4) {
        string title = argv[1];
        string category = argv[2];
        string desc = argv[3];

        ComplaintManager manager;
        manager.saveComplaint(title, category, desc);
    } else {
        cout << "Invalid Arguments";
    }
    return 0;
}