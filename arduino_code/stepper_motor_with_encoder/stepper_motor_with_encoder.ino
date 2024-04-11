String myCmd;
int n[3];

const int baseDIR = 2;
const int basePUL = 3;

const int wristDIR = 4;
const int wristPUL = 5;

const int gripperDIR = 7;
const int gripperPUL = 6;

const int base_encoder = A0;
const int wrist_encoder = A1;
const int gripper_encoder = A2;

int base_encoder_upperlimit = 270;
int wrist_encoder_upperlimit = 270;
int gripper_encoder_upperlimit = 270;

void setup() 
{
  
  Serial.begin(115200);
  
  pinMode(baseDIR,OUTPUT);
  pinMode(basePUL,OUTPUT);

  pinMode(wristDIR,OUTPUT);
  pinMode(wristPUL,OUTPUT);

  pinMode(gripperDIR,OUTPUT);
  pinMode(gripperPUL,OUTPUT);
  
}

void loop()
{
  while(Serial.available()!=0)
  {
    int i=0,s=0,c=0;
    myCmd=Serial.readStringUntil('\r');
    int l = myCmd.length();
    for(i=0;i<l;i++)
    {
      if(myCmd.charAt(i)==',')
      {
        n[c]=(myCmd.substring(s,i)).toInt();
        s=i+1;
        c++;
      }
    }
  }  
  int base_desired_angle = n[0];
  int wrist_desired_angle = n[1];
  int gripper_desired_angle = n[2];
  
  stepper_motor_angle_adjuster(baseDIR,basePUL,base_desired_angle,base_encoder);
  stepper_motor_angle_adjuster(wristDIR,wristPUL,wrist_desired_angle,wrist_encoder);
  stepper_motor_angle_adjuster(gripperDIR,gripperPUL,gripper_desired_angle,gripper_encoder);
  
}
void stepper_motor_angle_adjuster(const int dir_Pin,const int pul_Pin,int desired_angle,const int encoder_Pin)
{
  
  int current_angle = map(analogRead(encoder_Pin),0,1023,0,270);

  if(current_angle > desired_angle)
  { 
    digitalWrite(dir_Pin, HIGH);
    digitalWrite(pul_Pin, HIGH);
    delayMicroseconds(500);
    digitalWrite(pul_Pin,LOW);
    delayMicroseconds(500);
  }
  else if(current_angle < desired_angle)
  {
    digitalWrite(dir_Pin, LOW);
    digitalWrite(pul_Pin, HIGH);
    delayMicroseconds(500);
    digitalWrite(pul_Pin,LOW);
    delayMicroseconds(500);
  }
  else
  {
    Serial.println("Motor has reached into desired angle");
  }
  
}
