#include <iostream>
using namespace std;

int main() {
    int i;
    for(i=1;i<=5;i++){
        for(int j=i;j<=5;j++){
            cout<<j;
        }
        for(int j=1;j<=(i-1);j++){
            cout<<j;
        }
        cout<<endl;
    }
  

    return 0;
}
