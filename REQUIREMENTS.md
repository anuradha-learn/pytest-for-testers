# NexaDesk Lite: Requirements

NexaDesk is the IT and HR service desk for Nexa Group employees.
These are the rules the team agreed. Your tests check that the app follows them.

## Tickets

1. Every ticket has a **title**, a **category** and a **priority**.
2. The **title** must be **5 to 100 characters** long (both included).
3. The **category** must be **IT** or **HR**.
4. The **priority** must be **P1**, **P2** or **P3**. If no priority is given, it is **P3**.
5. A new ticket starts with the status **open**.
6. Each priority has a promised response time:

   | Priority | Meaning | Response time |
   |---|---|---|
   | P1 | Urgent | 4 hours |
   | P2 | High | 1 day (24 hours) |
   | P3 | Normal | 3 days (72 hours) |

7. Tickets that break a rule are rejected with status **422**, and nothing is saved.
8. Asking for a ticket that does not exist returns status **404**.

## Assistant

The NexaDesk assistant answers common employee questions in plain language.
Its wording can change from one answer to the next, but the facts must not.

| Topic | Facts every answer must include |
|---|---|
| Password reset | Use the IT portal; works within 15 minutes |
| Annual leave | 30 days per year; book in the HR portal |
| New laptop | Raise an IT ticket; delivered within 5 working days |
| Response times | P1 4 hours, P2 1 day, P3 3 days |
| Anything else | Tell the employee to raise a ticket |

Every answer must also:

- say which **topic** it answered
- be short: no more than **200 characters**