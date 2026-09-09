import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Academia | School management",
  description: "A focused school management dashboard for every role.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
