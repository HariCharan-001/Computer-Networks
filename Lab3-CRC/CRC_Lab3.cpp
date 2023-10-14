#include <bits/stdc++.h>
using namespace std;
#define cout out

ofstream out;

bitset <136> generate_random_error(bitset <136> error){
    int len = 136;
    error = 0;

    while(len--)
        error[len] = rand() % 2;

    return error;
}

bitset <9> modulo2div(bitset <136> message, bitset <9> generator){
    bitset <9> rem ((message >> (136-9)).to_ulong());
    bitset <9> zero(0);
    message <<= 8;
    
    int reps = 136 - 9 + 1;
    while(reps--){
        if(rem[8] == 1)
            rem ^= generator;
        else
            rem ^= zero;

        if(reps == 0)
            break;

        message <<= 1; 
        rem <<= 1;
        if(message[135] == 1)
            rem[0] = 1;
    }

    return rem;
}

void check_corrupted(bitset <136> message, bitset <9> generator){
    if(modulo2div(message, generator).to_ulong() == 0)
        cout<<"CRC check: Failed\n\n";
    else
        cout<<"CRC check: Passed\n\n";
}

int main(int argc, char * argv[]){
    srand(time(NULL));
    ifstream in(argv[1]);
    out.open(argv[2]);

    while(!in.eof()){
        int d = 128;
        bitset <128> message;
        in>>message;

        // generator x^8 + x^2 + x + 1 (8+1 bits)
        int r = 8;
        bitset <9> generator("100000111");

        //append r 0's to message
        bitset <128 + 8> CRC(message.to_string() + string(r, '0'));

        // calculate the remainder of message when divided by generator (modulo 2 division)
        bitset <136> rem = (modulo2div(CRC, generator)).to_ulong();

        // remainder xor message
        CRC ^= rem;

        cout<<"Input: "<<message<<endl;
        cout<<"CRC (Remainder): "<<(rem.to_string()).substr(128)<<endl<<endl;

        cout<<"Random Bit Errors \n\n";
        int reps = 10;
        while(reps--){
            cout<<"Original string: "<<message<<endl;
            cout<<"Original string with CRC: "<<CRC<<endl;
        
            bitset <136> error(0);
            while(error.count() < 3 || error.count() % 2 == 0)
                error = generate_random_error(error);
            
            bitset <136> corrupted(error);
            corrupted ^= CRC;

            cout<<"Corrupted string: "<<corrupted<<endl;
            cout<<"No of errors introduced: "<<error.count()<<endl;
            check_corrupted(corrupted, generator);
        }

        cout<<"Bursty Bit Errors \n\n";
        reps = 5;
        while(reps--){
            cout<<"Original string: "<<message<<endl;
            cout<<"Original string with CRC: "<<CRC<<endl;
        
            //random bursty error of length 6 with starting bit error position 100 - 110
            bitset <136> error("111111");
            int shift = 26 + rand()%11;
            error <<= shift;

            bitset <136> corrupted(error);
            corrupted ^= CRC;

            cout<<"Corrupted string: "<<corrupted<<endl;
            cout<<"No of errors introduced: "<<6<<endl;
            check_corrupted(corrupted, generator);
        }

        cout<<"\n\n\n";
    }
}