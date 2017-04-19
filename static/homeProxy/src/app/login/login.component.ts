/**
 * Created by LifenetsAndrew on 10.04.17.
 */
import {Component} from '@angular/core';
import {LoginService} from '../services/login.service'

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  providers: [LoginService]
})
export class LoginComponent {
  private login: string;
  private password: string;

  constructor(private loginService: LoginService){

  }

  public doLogin() {
    this.loginService.doLogin(this.login, this.password).subscribe(this.logined);
  }

  public logined(){
    console.log("Logined");
  }
}
