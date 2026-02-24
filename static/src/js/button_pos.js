/** @odoo-module **/
import { Component, onMounted,onUnmounted, useRef, useState } from "@odoo/owl";


export class CharCounter extends Component {
    static template = "CharCounter";

    setup() {
        // 1. Create the reference for the textarea
        this.textareaRef = useRef("myTextarea");
        
        // 2. Track the count in a reactive state
        this.state = useState({ count: 0 });

        onMounted(() => {
            // 3. Access the real DOM element via .el
            const el = this.textareaRef.el;
            
            // 4. Attach a listener to update the count as the user types
            this.onInput = (ev) => {
                this.state.count = ev.target.value.length;
            };
            el.addEventListener("input", this.onInput);
            
            console.log("Counter is active! connected to textarea:", el);
        });

        onUnmounted(() => {
            // Clean up the event listener when the component is destroyed
            const el = this.textareaRef.el;
            el.removeEventListener("input", this.onInput);
        });

        
    }
}


































// import { Component, onRendered } from "@odoo/owl";
// import { registry } from "@web/core/registry";

// export class MyComponent extends Component {
//     setup() {
//         // onRendered is called inside setup()
//         onRendered(() => {
//             console.log("Component template has been rendered and DOM is updated.");
            
//             // Example: Accessing a DOM element directly
//             // const element = document.querySelector(".my-element");
//             // console.log("Element height:", element.offsetHeight);
//         });
//     }
// }
// MyComponent.template = "MyComponentTemplate";
// registry.category("actions").add("MyComponent", MyComponent);







// import { Component, useState } from "@odoo/owl";
// import { registry } from "@web/core/registry";

// export class ButtonPos extends Component {
//     static template = "ButtonPos";

//     setup() {
//         // 1. Get saved value from browser or default to 1
//         const savedValue = localStorage.getItem("my_button_count");
//         const initialCount = savedValue ? parseInt(savedValue) : 1;

//         // 2. Define the reactive state
//         this.state = useState({
//             count: initialCount,
//         });

//         this.c = initialCount;
//     }

//     Increment() {
//         this.state.count += 1; 
//         this.c += 1;           
        
//         // Save to browser memory
//         localStorage.setItem("my_button_count", this.state.count);
        
//         console.log("State updated to:", this.state.count);
//         console.log("C updated to:", this.c);
//     }
// }

// registry.category("actions").add("ButtonPos", ButtonPos);
