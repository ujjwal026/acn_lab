import socket
def xor(a,b):
    res=''
    for i in range(len(a)):
        res+=str(int(a[i])^int(b[i]))
    return res

def checksum_(message,generator):
    padded_msg=message+'0'*(len(generator)-1)
    rem=padded_msg
    while len(rem)>=len(generator):
        if rem[0]=='1':
                rem=xor(rem[:len(generator)],generator)+rem[len(generator):]
        else:
            rem=rem[1:]
    return rem
def sender():
    message=input("Enter the message ")
    gen=input("enter the generator")
    csum=checksum_(message,gen)
    print(f'checksum code:',csum)
    return message,gen,csum
def recever(message,gen,csum):
    c_sum=csum
    test_msg=message+c_sum
    validity=checksum_(test_msg,gen)
    print("Recived checksum",validity)
    if validity=='0'*(len(gen)-1):
         print("data is valid")
    else:
        print("data is invalid")
def main():
    print("Sender:")
    message,gen,csum=sender()
    print("Receiver:")
    recever(message,gen,csum)

if __name__=="__main__":
  main()

         
